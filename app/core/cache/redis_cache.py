import json
from functools import wraps
from typing import Any, Callable, List, Optional

from app.configs.cache_config import cache_config
from app.core.context.redis_context import RedisContext
from app.core.data.data_response import DataResponse
from app.core.logs.logging import get_logger

from .redis_key_builder import (default_key_builder, request_key_builder,
                                result_key_builder)

logger = get_logger(__name__)
_config = cache_config()


async def init():
    logger.info('Initializing redis cache...')

    RedisContext.init(_config)

    logger.info('Redis cache initialized!')


async def close():
    logger.info('Closing redis cache...')

    await RedisContext.close()

    logger.info('Redis cache closed!')


def cache_get(
    namespace: str,
    identifier='id',
    key_builder=request_key_builder
):
    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            kwargs_copy = kwargs.copy()
            request = kwargs_copy.pop("request", None)
            response = kwargs_copy.pop("response", None)
            key = get_key(
                func=func,
                namespace=namespace,
                identifier=identifier,
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


def cache_put(
    namespace: str,
    identifier='id',
    key_builder=result_key_builder
):
    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            kwargs_copy = kwargs.copy()
            request = kwargs_copy.pop("request", None)
            result = await func(*args, **kwargs)

            if is_no_store(request):
                return result

            key = get_key(
                func=func,
                namespace=namespace,
                identifier=identifier,
                result=result,
                args=args,
                kwargs=kwargs_copy,
                key_builder=key_builder
            )

            await set(key, result)

            return result

        return inner

    return wrapper


def cache_evict(
    namespace: str,
    identifier='id',
    key_builder=request_key_builder
):
    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            key = get_key(
                func=func,
                namespace=namespace,
                identifier=identifier,
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
    identifier: Optional[str],
    key_builder: Optional[Callable],
    result: Optional[DataResponse] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None
):
    key_builder = key_builder or default_key_builder

    return key_builder(
        func=func,
        namespace=namespace,
        identifier=identifier,
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

    await RedisContext.instance.set(key, value, _config.ttl)


async def get(key: str):
    value = await RedisContext.instance.get(key)

    return json.loads(value) if value else None


async def delete(keys: List[str]):
    await RedisContext.instance.delete(keys)


async def get_with_ttl(key: str):
    async with RedisContext.instance.pipeline(transaction=True) as pipe:
        value, ttl = await (pipe.get(key).ttl(key).execute())
        value = json.loads(value) if value else None

        return value, ttl
