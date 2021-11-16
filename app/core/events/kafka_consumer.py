import json
from asyncio import create_task
from typing import Awaitable

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord
from app.configs.constants import TOPIC_SAMPLE_CREATE
from app.configs.kafka_config import kafka_config
from app.core.logs.logging import get_logger
from app.events import sample_consumer

logger = get_logger(__name__)
_kafka_config = kafka_config()

topic = {
    TOPIC_SAMPLE_CREATE: sample_consumer.create
}


async def init():
    for key, value in topic.items():
        create_task(consume(key, value))


def string_deserializer(value: bytes):
    return value.decode('utf-8')


def json_deserializer(value: bytes):
    if not value:
        return None

    return json.loads(value.decode('utf-8'))


async def consume(
    topic: str,
    callback: Awaitable,
    value_deserializer=json_deserializer,
    auto_offset_reset='earliest'
):
    logger.info(f"Initializing kafka consumer for topic {topic}...")

    consumer = AIOKafkaConsumer(
        topic,
        client_id=_kafka_config.client_id,
        group_id=_kafka_config.group_id,
        bootstrap_servers=_kafka_config.brokers,
        value_deserializer=value_deserializer,
        auto_offset_reset=auto_offset_reset
    )

    await consumer.start()

    logger.info(f"Kafka consumer for topic {topic} initialized!")

    try:
        message: ConsumerRecord

        async for message in consumer:
            log = "Consuming {}:{}:{} key={} value={}".format(
                message.topic,
                message.partition,
                message.offset,
                message.key,
                message.value
            )
            logger.info(log)

            await callback(message)
    finally:
        logger.info(f"Stopping Kafka consumer for topic {topic}...")

        await consumer.stop()

        logger.info(f"Kafka consumer for topic {topic} stopped!")
