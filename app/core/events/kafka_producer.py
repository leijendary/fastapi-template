import json
from typing import Any, Dict

from aiokafka import AIOKafkaProducer
from app.configs.kafka_config import kafka_config
from app.core.logs.logging import get_logger

logger = get_logger(__name__)
config = kafka_config()


def json_serializer(value: Any):
    if not value:
        return None

    return json.dumps(value).encode('utf-8')


async def send(topic: str, value: Dict = None, key: str = None):
    producer = AIOKafkaProducer(
        client_id=config.client_id,
        bootstrap_servers=config.brokers,
        enable_idempotence=True
    )

    await producer.start()

    try:
        json_value = json_serializer(value)

        await producer.send_and_wait(topic, json_value, key)

        logger.info(f"Sent to topic {topic} with key={key} and value={value}")
    finally:
        await producer.stop()
