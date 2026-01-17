import json
from typing import Any

import pika

from app.config import settings


def publish_event(payload: dict[str, Any]) -> None:
    connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.rabbitmq_exchange, exchange_type="topic", durable=True)
    channel.basic_publish(
        exchange=settings.rabbitmq_exchange,
        routing_key=settings.rabbitmq_routing_key,
        body=json.dumps(payload).encode("utf-8"),
        properties=pika.BasicProperties(content_type="application/json"),
    )
    connection.close()
