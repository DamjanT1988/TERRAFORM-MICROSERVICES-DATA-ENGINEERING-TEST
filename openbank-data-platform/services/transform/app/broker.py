import json
from typing import Callable

import pika

from app.config import settings


def start_consumer(on_message: Callable[[dict], None], max_messages: int | None = None) -> None:
    connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.rabbitmq_exchange, exchange_type="topic", durable=True)
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)
    channel.queue_bind(
        queue=settings.rabbitmq_queue,
        exchange=settings.rabbitmq_exchange,
        routing_key=settings.rabbitmq_routing_key,
    )

    processed = {"count": 0}

    def _callback(ch, method, properties, body):  # noqa: ANN001
        payload = json.loads(body.decode("utf-8"))
        on_message(payload)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        processed["count"] += 1
        if max_messages is not None and processed["count"] >= max_messages:
            ch.stop_consuming()

    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=_callback)
    channel.start_consuming()
    connection.close()
