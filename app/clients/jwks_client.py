from app.configs.security_config import security_config
from app.core.clients.httpx_client import client
from app.core.logs.logging import get_logger
from fastapi_cache.decorator import cache

logger = get_logger(__name__)
security_config = security_config()
jwks_url = security_config.jwks_url


@cache(namespace=security_config.jwks_cache_key)
async def keys():
    logger.info(f"Getting jwks from {jwks_url}")

    response = await client.get(jwks_url)

    return response.json()['keys']
