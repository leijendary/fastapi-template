from functools import lru_cache

from aiocache import Cache
from aiocache import cached as aio_cached
from aiocache import caches
from pydantic import BaseSettings


class CacheConfig(BaseSettings):
    redis_host: str
    redis_port = 6379
    ttl = 43200

    class Config:
        env_prefix = 'cache_'
        env_file = '.env'


@lru_cache
def cache_config():
    return CacheConfig()


config = cache_config()

caches.set_config({
    'default': {
        'cache': 'aiocache.RedisCache',
        'endpoint': config.redis_host,
        'port': config.redis_port,
        'serializer': {'class': 'aiocache.serializers.JsonSerializer'},
        'plugins': [
            {'class': 'aiocache.plugins.HitMissRatioPlugin'},
            {'class': 'aiocache.plugins.TimingPlugin'}
        ]
    }
})


def cached(key: str, ttl=config.ttl, cache=Cache.REDIS):
    return aio_cached(key=key, ttl=ttl, cache=cache)
