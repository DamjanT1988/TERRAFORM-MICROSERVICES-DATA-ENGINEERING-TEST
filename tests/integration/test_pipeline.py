import os
import threading
import time
from pathlib import Path

import base64
import io
import http.client
import json
import urllib.request
import urllib.error
import pika
import sys
from minio import Minio
from testcontainers.minio import MinioContainer
from testcontainers.postgres import PostgresContainer
from testcontainers.core.container import DockerContainer
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text


def _wait_for_rabbitmq(host: str, amqp_port: int, mgmt_port: int) -> None:
    deadline = time.time() + 120
    auth = base64.b64encode(b"guest:guest").decode("ascii")
    while time.time() < deadline:
        try:
            req = urllib.request.Request(
                f"http://{host}:{mgmt_port}/api/healthchecks/node",
                headers={"Authorization": f"Basic {auth}"},
            )
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    payload = json.loads(response.read().decode("utf-8"))
                    if payload.get("status") == "ok":
                        return
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            json.JSONDecodeError,
            http.client.RemoteDisconnected,
            ConnectionResetError,
            ConnectionAbortedError,
        ):
            time.sleep(1)
    raise RuntimeError("RabbitMQ did not become ready")


def test_ingest_transform_api_pipeline() -> None:
    root = Path(__file__).resolve().parents[2]
    csv_path = root / "data" / "transactions_raw.csv"
    sys.path.append(str(root / "services" / "transform"))

    with PostgresContainer("postgres:15") as postgres:
        with MinioContainer("minio/minio:RELEASE.2024-08-17T01-24-54Z") as minio:
            rabbitmq = DockerContainer("rabbitmq:3.13-management").with_exposed_ports(5672, 15672)
            try:
                rabbitmq.start()

                rabbit_host = rabbitmq.get_container_host_ip()
                rabbit_port = int(rabbitmq.get_exposed_port(5672))
                rabbit_mgmt_port = int(rabbitmq.get_exposed_port(15672))
                _wait_for_rabbitmq(rabbit_host, rabbit_port, rabbit_mgmt_port)

                minio_host = minio.get_container_host_ip()
                minio_port = int(minio.get_exposed_port(9000))

                os.environ["TRANSFORM_MINIO_ENDPOINT"] = f"{minio_host}:{minio_port}"
                os.environ["TRANSFORM_MINIO_ACCESS_KEY"] = minio.access_key
                os.environ["TRANSFORM_MINIO_SECRET_KEY"] = minio.secret_key
                os.environ["TRANSFORM_MINIO_BUCKET"] = "raw-transactions"
                os.environ["TRANSFORM_RABBITMQ_URL"] = (
                    f"amqp://guest:guest@{rabbit_host}:{rabbit_port}/"
                )
                os.environ["TRANSFORM_DATABASE_URL"] = postgres.get_connection_url()

                alembic_cfg = Config(str(root / "services" / "transform" / "alembic.ini"))
                alembic_cfg.set_main_option(
                    "script_location", str(root / "services" / "transform" / "migrations")
                )
                alembic_cfg.set_main_option("sqlalchemy.url", postgres.get_connection_url())
                command.upgrade(alembic_cfg, "head")

                client = Minio(
                    os.environ["TRANSFORM_MINIO_ENDPOINT"],
                    access_key=minio.access_key,
                    secret_key=minio.secret_key,
                    secure=False,
                )
                if not client.bucket_exists("raw-transactions"):
                    client.make_bucket("raw-transactions")

                object_key = "csv/test-transactions.csv"
                payload = csv_path.read_bytes()
                client.put_object(
                    "raw-transactions",
                    object_key,
                    data=io.BytesIO(payload),
                    length=len(payload),
                    content_type="text/csv",
                )

                import importlib

                from services.transform.app import broker, worker

                importlib.reload(broker)
                importlib.reload(worker)

                thread = threading.Thread(
                    target=broker.start_consumer, args=(worker._process_message, 1), daemon=True
                )
                thread.start()

                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=rabbit_host, port=rabbit_port)
                )
                channel = connection.channel()
                channel.exchange_declare(exchange="transactions", exchange_type="topic", durable=True)
                channel.basic_publish(
                    exchange="transactions",
                    routing_key="ingest.created",
                    body=f'{{"object_key": "{object_key}"}}'.encode("utf-8"),
                )
                connection.close()

                thread.join(timeout=20)
                assert thread.is_alive() is False

                engine = create_engine(postgres.get_connection_url())
                with engine.connect() as connection:
                    count = connection.execute(text("select count(*) from curated_transactions")).scalar()
                assert count > 0
            finally:
                rabbitmq.stop()
