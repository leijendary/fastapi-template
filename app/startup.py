from fastapi import FastAPI

from app.core.cache import redis_setup
from app.core.messaging import kafka_setup
from app.core.monitoring import tracing
from app.core.search import elasticsearch_setup
from app.documents import sample_document
from app.messaging import sample_consumer
from app.models import model

functions = [
    tracing.init,
    model.init,
    elasticsearch_setup.init,
    kafka_setup.init,
    redis_setup.init,
    sample_consumer.init,
    sample_document.init,
]


def add_handlers(app: FastAPI):
    [app.add_event_handler("startup", function) for function in functions]
