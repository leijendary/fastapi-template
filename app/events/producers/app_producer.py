import json
from typing import Any, Dict

from aiokafka import AIOKafkaProducer
from app.configs.kafka import kafka_config
from app.configs.logging import get_logger

logger = get_logger(__name__)
config = kafka_config()


def json_serializer(value: Any):
    if not value:
        return None

    return json.dumps(value).encode('utf-8')


async def produce(topic: str, value: Dict = None, key: str = None):
    producer = AIOKafkaProducer(
        client_id=config.kafka_client_id,
        bootstrap_servers=config.kafka_brokers,
        enable_idempotence=True
    )

    await producer.start()

    try:
        json_value = json_serializer(value)

        await producer.send_and_wait(topic, json_value, key)

        logger.info(f"Sent to topic {topic} with key={key} and value={value}")
    finally:
        await producer.stop()
