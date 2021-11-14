import json
from functools import wraps
from typing import Any, Callable, List, Optional

from aioredis import from_url
from app.configs.cache_config import cache_config
from app.core.data.data_response import DataResponse
from app.core.logs.logging import get_logger

from .redis_key_builder import (default_key_builder, request_key_builder,
                                result_key_builder)

logger = get_logger(__name__)
config = cache_config()
scheme = 'rediss' if config.use_ssl else 'redis'

redis = from_url(
    f"{scheme}://{config.redis_host}:{config.redis_port}",
    username=config.username,
    password=config.password,
    decode_responses=True
)


async def close():
    logger.info('Closing redis cache...')

    await redis.close()

    logger.info('Redis cache closed!')


def cache_get(namespace: str, key_builder=request_key_builder):
    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            nonlocal key_builder
            kwargs_copy = kwargs.copy()
            request = kwargs_copy.pop("request", None)
            response = kwargs_copy.pop("response", None)
            key = get_key(
                func=func,
                namespace=namespace,
                args=args,
                kwargs=kwargs_copy,
                key_builder=key_builder
            )
            result, ttl = await get_with_ttl(key)

            if result:
                if response:
                    return with_headers(result, ttl, request, response)

                return result

            result = await func(*args, **kwargs)

            if not result or is_no_store(request):
                return result

            await set(key, result)

            return result

        return inner

    return wrapper


def cache_put(namespace: str, key_builder=result_key_builder):
    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            nonlocal key_builder
            kwargs_copy = kwargs.copy()
            request = kwargs_copy.pop("request", None)
            result = await func(*args, **kwargs)

            if is_no_store(request):
                return result

            key = get_key(
                func=func,
                namespace=namespace,
                result=result,
                args=args,
                kwargs=kwargs_copy,
                key_builder=key_builder
            )

            await set(key, result)

            return result

        return inner

    return wrapper


def cache_evict(namespace: str, key_builder=request_key_builder):
    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            nonlocal key_builder

            key = get_key(
                func=func,
                namespace=namespace,
                args=args,
                kwargs=kwargs,
                key_builder=key_builder
            )

            await delete(key)

            return await func(*args, **kwargs)

        return inner

    return wrapper


def get_key(
    func,
    namespace: str,
    key_builder: Optional[Callable],
    result: Optional[DataResponse] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None
):
    key_builder = key_builder or default_key_builder

    return key_builder(
        func=func,
        namespace=namespace,
        result=result,
        args=args,
        kwargs=kwargs
    )


def with_headers(request, ttl, response, result):
    etag = f"W/{hash(result)}"
    response.headers["Cache-Control"] = f"max-age={ttl}"
    response.headers["ETag"] = etag

    if not request:
        return response

    if_none_match = request.headers.get("if-none-match")

    if if_none_match == etag:
        response.status_code = 304

    return response


def is_no_store(request):
    return request and request.headers.get("Cache-Control") == "no-store"


async def set(key: str, value: Any):
    if hasattr(value, 'json'):
        value = value.json()
    else:
        value = json.dumps(value)

    await redis.set(key, value, config.ttl)


async def get(key: str):
    value = await redis.get(key)

    return json.loads(value)


async def delete(keys: List[str]):
    await redis.delete(keys)


async def get_with_ttl(key: str):
    async with redis.pipeline(transaction=True) as pipe:
        value, ttl = await (pipe.get(key).ttl(key).execute())
        value = json.loads(value) if value else None

        return value, ttl
