from app.configs.security_config import security_config
from app.core.cache.redis_cache import cache_get
from app.core.context.httpx_context import HttpxClientContext
from app.core.logs.logging import get_logger

logger = get_logger(__name__)
_config = security_config()


@cache_get(namespace='fastapi:jwks', key_builder=None)
async def keys():
    jwks_url = _config.jwks_url

    logger.info(f"Getting jwks from {jwks_url}")

    response = await HttpxClientContext.instance.get(jwks_url)

    return response.json()['keys']
