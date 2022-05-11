from app.core.cache import redis_cache
from app.core.databases import main_sql
from app.core.messaging import kafka_producer
from app.core.search import elasticsearch
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"]
)


@router.get(path="/", status_code=200)
async def healthcheck():
    body = {
        "status": "UP",
        "database": await main_sql.health(),
        "elasticsearch": await elasticsearch.health(),
        "kafka": await kafka_producer.health(),
        "redis": await redis_cache.health()
    }
    status_code = 200 if "DOWN" not in body.values() else 503

    return JSONResponse(body, status_code)
