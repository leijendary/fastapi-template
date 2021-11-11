import json
from asyncio import create_task
from typing import Awaitable

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord
from app.configs.kafka import kafka_config
from app.configs.logging import get_logger
from app.events.consumers import sample_consumer
from app.events.topic import SAMPLE_CREATE

logger = get_logger(__name__)
config = kafka_config()


topic = {
    SAMPLE_CREATE: sample_consumer.create
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
