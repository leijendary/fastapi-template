from app.configs.cache_config import cache_config
from app.configs.client_config import client
from app.configs.security_config import security_config
from fastapi_cache.decorator import cache

security_config = security_config()
cache_config = cache_config()
jwks_url = security_config.jwks_url


@cache(namespace=security_config.jwks_cache_key)
async def keys():
    print(f"Calling jwks url: {jwks_url}")

    response = await client.get(jwks_url)

    return response.json()['keys']
