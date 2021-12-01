import json
from typing import Any, Dict

from app.configs.kafka_config import kafka_config
from app.core.context.kafka_context import KafkaProducerContext
from app.core.logs.logging import get_logger

logger = get_logger(__name__)


async def init():
    logger.info('Starting kafka producer...')

    await KafkaProducerContext.init(kafka_config())

    logger.info('Kafka producer started!')


async def close():
    logger.info('Stopping kafka producer...')

    await KafkaProducerContext.close()

    logger.info('Kafka producer stopped!')


def json_serializer(value: Any):
    if not value:
        return None

    return json.dumps(value).encode('utf-8')


async def send(topic: str, value: Dict = None, key: str = None):
    json_value = json_serializer(value)

    await KafkaProducerContext.instance.send_and_wait(topic, json_value, key)

    logger.info(f"Sent to topic {topic} key={key} value={value}")
