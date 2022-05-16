from asyncio import create_task

from aiokafka.structs import ConsumerRecord

from app.constants import (TOPIC_SAMPLE_CREATE, TOPIC_SAMPLE_DELETE,
                           TOPIC_SAMPLE_UPDATE)
from app.core.messaging.kafka_consumer import consume


async def create(message: ConsumerRecord):
    pass


async def update(message: ConsumerRecord):
    pass


async def delete(message: ConsumerRecord):
    pass


_topics = {
    TOPIC_SAMPLE_CREATE: create,
    TOPIC_SAMPLE_UPDATE: update,
    TOPIC_SAMPLE_DELETE: delete,
}


async def init():
    [create_task(consume(key, value)) for key, value in _topics.items()]
