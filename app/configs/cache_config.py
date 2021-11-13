from functools import lru_cache

from pydantic import BaseSettings


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
