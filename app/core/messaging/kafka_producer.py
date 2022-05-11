import json
from typing import Any, Dict

from aiokafka.producer.producer import AIOKafkaProducer
from app.core.configs.kafka_config import KafkaConfig, kafka_config
from app.core.logs.logging import get_logger

_config = kafka_config()
logger = get_logger(__name__)


class KafkaProducer:
    instance: AIOKafkaProducer

    @classmethod
    async def init(self):
        self.instance = AIOKafkaProducer(
            client_id=_config.client_id,
            bootstrap_servers=_config.brokers,
            enable_idempotence=True
        )
        await self.instance.start()


def producer() -> AIOKafkaProducer:
    return KafkaProducer.instance


async def init():
    logger.info("Starting kafka producer...")

    await KafkaProducer.init()

    logger.info("Kafka producer started!")


async def close():
    logger.info("Stopping kafka producer...")

    await producer().stop()

    logger.info("Kafka producer stopped!")


async def health():
    try:
        version = await producer().client.check_version()

        return "UP" if version else "DOWN"
    except:
        return "DOWN"


def json_serializer(value: Any):
    if not value:
        return None

    return json.dumps(value).encode("utf-8")


async def send(topic: str, value: Dict = None, key: str = None):
    json_value = json_serializer(value)

    await producer().send_and_wait(topic, json_value, key)

    logger.info(f"Sent to topic {topic} key={key} value={value}")
