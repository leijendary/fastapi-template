from fastapi import FastAPI

from app.core.cache import redis_cache
from app.core.messaging import kafka_producer
from app.core.search import elasticsearch
from app.documents import sample_document
from app.messaging import sample_consumer
from app.models import model

functions = [
    model.init,
    elasticsearch.init,
    kafka_producer.init,
    redis_cache.init,
    sample_consumer.init,
    sample_document.init,
]


def add_handlers(app: FastAPI):
    [app.add_event_handler("startup", function) for function in functions]
