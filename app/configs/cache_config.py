from functools import lru_cache
from typing import Optional

from aioredis import from_url
from app.configs.logging_config import get_logger
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseSettings
from starlette.requests import Request
from starlette.responses import Response

logger = get_logger(__name__)


class CacheConfig(BaseSettings):
    redis_host: str
    redis_port = 6379
    username: str = None
    password: str = None
    use_ssl = False
    ttl = 43200
    max_connections = 10

    class Config:
        env_prefix = 'cache_'
        env_file = '.env'


@lru_cache
def cache_config():
    return CacheConfig()


def key_builder(
    func,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    return namespace


config = cache_config()
scheme = 'rediss' if config.use_ssl else 'redis'
credentials = ''

if config.username and config.password:
    credentials = f"{config.username}:{config.password}@"

redis = from_url(
    f"{scheme}://{credentials}{config.redis_host}:{config.redis_port}",
    decode_responses=True,
    max_connections=config.max_connections
)


async def init():
    logger.info('Initializing redis cache...')

    FastAPICache.init(
        RedisBackend(redis),
        expire=config.ttl,
        key_builder=key_builder
    )

    logger.info('Redis cache initialized!')


async def close():
    logger.info('Closing redis cache...')

    await redis.close()

    logger.info('Redis cache closed!')
