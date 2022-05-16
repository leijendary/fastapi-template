from app.core.cache.redis_cache import cache_get, redis
from app.core.clients.httpx_client import async_client
from app.core.configs.security_config import security_config
from app.core.logs.logging_setup import get_logger
from app.core.utils.thread_util import synchronized

logger = get_logger(__name__)
_config = security_config()
_cache_key = _config.jwks_cache_key
_jwks_url = _config.jwks_url
_client = async_client(base_url=_jwks_url)


@cache_get(namespace=_cache_key, key_builder=None)
async def keys():
    return await _fetch_keys()


@synchronized
async def _fetch_keys():
    cached = await redis().get(_cache_key)

    if cached:
        return cached

    logger.info(f"Getting jwks from {_jwks_url}")

    response = await _client.get("")

    return response.json()["keys"]


async def close():
    await _client.aclose()
