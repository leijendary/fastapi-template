from app.configs.security_config import security_config
from app.core.cache.redis_cache import cache_get
from app.core.clients.httpx_client import client
from app.core.logs.logging import get_logger

logger = get_logger(__name__)
security_config = security_config()
jwks_url = security_config.jwks_url


@cache_get(namespace='fastapi:jwks', key_builder=None)
async def keys():
    logger.info(f"Getting jwks from {jwks_url}")

    response = await client.get(jwks_url)

    return response.json()['keys']
