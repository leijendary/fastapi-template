import json
from typing import Any, Dict, Type

from aiokafka.producer.producer import AIOKafkaProducer

from app.core.configs.kafka_config import kafka_config
from app.core.logs.logging_setup import get_logger
from app.core.monitoring.tracing import single_span

_config = kafka_config()
logger = get_logger(__name__)


class KafkaProducer:
    instance: AIOKafkaProducer

    @classmethod
    async def init(cls):
        cls.instance = AIOKafkaProducer(
            client_id=_config.client_id,
            bootstrap_servers=_config.brokers,
            enable_idempotence=True,
            value_serializer=json_serializer
        )
        await cls.instance.start()

    @classmethod
    async def send(cls, topic: str, value: Dict, key: str = None):
        span = single_span()
        headers = [("b3", span.encode("utf-8"))]

        await cls.instance.send(topic, value, key, headers=headers)

        logger.info(f"Sent to topic {topic} key={key} value={value}")


def producer() -> Type[KafkaProducer]:
    return KafkaProducer


async def init():
    logger.info("Starting kafka producer...")

    await KafkaProducer.init()

    logger.info("Kafka producer started!")


async def close():
    logger.info("Stopping kafka producer...")

    await KafkaProducer.instance.stop()

    logger.info("Kafka producer stopped!")


async def health():
    try:
        version = await KafkaProducer.instance.client.check_version()

        return "UP" if version else "DOWN"
    except:
        return "DOWN"


def json_serializer(value: Any):
    if not value:
        return None

    return json.dumps(value).encode("utf-8")
