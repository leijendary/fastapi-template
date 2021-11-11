import json
from asyncio import create_task
from functools import lru_cache
from typing import Any, Awaitable, Dict

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.structs import ConsumerRecord
from app.configs.constants import TOPIC_SAMPLE_CREATE
from app.configs.logging_config import get_logger
from app.events import sample_consumer
from pydantic import BaseSettings

logger = get_logger(__name__)

topic = {
    TOPIC_SAMPLE_CREATE: sample_consumer.create
}


class KafkaConfig(BaseSettings):
    kafka_client_id: str
    kafka_group_id: str
    kafka_brokers: str

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def kafka_config():
    return KafkaConfig()


config = kafka_config()


async def init():
    for key, value in topic.items():
        create_task(consume(key, value))


def string_deserializer(value: bytes):
    return value.decode('utf-8')


def json_deserializer(value: bytes):
    if not value:
        return None

    return json.loads(value.decode('utf-8'))


def json_serializer(value: Any):
    if not value:
        return None

    return json.dumps(value).encode('utf-8')


async def consume(
    topic: str,
    callback: Awaitable,
    value_deserializer=json_deserializer,
    auto_offset_reset='earliest'
):
    logger.info(f"Initializing Kafka consumer for topic {topic}...")

    consumer = AIOKafkaConsumer(
        topic,
        client_id=config.kafka_client_id,
        group_id=config.kafka_group_id,
        bootstrap_servers=config.kafka_brokers,
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
