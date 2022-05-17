from fastapi import FastAPI

from app.clients import google_client
from app.core.cache import redis_setup
from app.core.clients import jwks_client
from app.core.databases import postgres_setup
from app.core.messaging import kafka_setup
from app.core.search import elasticsearch_setup

functions = [
    postgres_setup.close,
    elasticsearch_setup.close,
    kafka_setup.close,
    redis_setup.close,
    google_client.close,
    jwks_client.close
]


def add_handlers(app: FastAPI):
    [app.add_event_handler("shutdown", function) for function in functions]
