from app.configs.security_config import security_config
from app.core.cache import redis_cache
from app.core.cache.redis_cache import cache_get
from app.core.context.httpx_context import HttpxClientContext
from app.core.logs.logging import get_logger
from app.core.utils.thread_util import synchronized

logger = get_logger(__name__)
_config = security_config()
_cache_key = _config.jwks_cache_key


@cache_get(namespace=_cache_key, key_builder=None)
async def keys():
    return await _fetch_keys()


@synchronized
async def _fetch_keys():
    cached = await redis_cache.get(_cache_key)

    if cached:
        return cached

    jwks_url = _config.jwks_url

    logger.info(f"Getting jwks from {jwks_url}")

    response = await HttpxClientContext.instance.get(jwks_url)

    return response.json()["keys"]
