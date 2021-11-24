from asyncio import create_task

from app.configs.constants import (TOPIC_SAMPLE_CREATE, TOPIC_SAMPLE_DELETE,
                                   TOPIC_SAMPLE_UPDATE)
from app.core.events.kafka_consumer import consume
from app.events import sample_consumer

topic = {
    TOPIC_SAMPLE_CREATE: sample_consumer.create,
    TOPIC_SAMPLE_UPDATE: sample_consumer.update,
    TOPIC_SAMPLE_DELETE: sample_consumer.delete,
}


async def init():
    for key, value in topic.items():
        create_task(consume(key, value))
