from asyncio import create_task

from app.events.consumers import sample_consumer
from app.events.consumers.app_consumer import create_consumer
from app.events.topic import SAMPLE_CREATE

topic = {
    SAMPLE_CREATE: sample_consumer.create
}


async def init():
    for key, value in topic.items():
        create_task(create_consumer(key, value))
