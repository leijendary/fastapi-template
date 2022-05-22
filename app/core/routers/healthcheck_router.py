from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.cache import redis_setup
from app.core.databases import postgres_setup
from app.core.messaging import kafka_setup
from app.core.search import elasticsearch_setup

router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"]
)


@router.get(path="/", response_model=Dict[str, str], status_code=200)
async def healthcheck():
    body = {
        "status": "UP",
        "database": await postgres_setup.health(),
        "elasticsearch": await elasticsearch_setup.health(),
        "kafka": await kafka_setup.health(),
        "redis": await redis_setup.health()
    }
    status_code = 200 if "DOWN" not in body.values() else 503

    return JSONResponse(body, status_code)
