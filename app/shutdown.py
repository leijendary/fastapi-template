from fastapi import FastAPI

from app.clients import google_client
from app.core.cache import redis_cache
from app.core.clients import jwks_client
from app.core.databases import main_sql
from app.core.messaging import kafka_producer
from app.core.search import elasticsearch

functions = [
    main_sql.close,
    elasticsearch.close,
    kafka_producer.close,
    redis_cache.close,
    google_client.close,
    jwks_client.close
]


def add_handlers(app: FastAPI):
    [app.add_event_handler("shutdown", function) for function in functions]
