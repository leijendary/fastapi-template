from aiocache import cached as aio_cached
from aiocache import Cache
from app.configs.cache_config import cache_config
from app.configs.client_config import client
from app.configs.security_config import security_config

security_config = security_config()
cache_config = cache_config()
jwks_url = security_config.jwks_url


@aio_cached(key="jwks", cache=Cache.REDIS, ttl=60)
async def keys():
    print(f"Calling jwks url: {jwks_url}")

    response = await client.get(jwks_url)

    return response.json()['keys']
