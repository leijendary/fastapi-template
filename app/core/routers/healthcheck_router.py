from app.core.context.elasticsearch_context import ElasticsearchContext
from app.core.context.kafka_context import KafkaProducerContext
from app.core.context.redis_context import RedisContext
from app.core.databases import tortoise_orm
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/healthcheck',
    tags=['healthcheck']
)


@router.get(path='/', status_code=200)
async def healthcheck():
    body = {
        'status': 'UP',
        'database': await tortoise_orm.health(),
        'elasticsearch': await ElasticsearchContext.health(),
        'kafka': await KafkaProducerContext.health(),
        'redis': await RedisContext.health()
    }
    status_code = 200 if 'DOWN' not in body.values() else 503

    return JSONResponse(body, status_code)
