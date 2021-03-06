import json
from functools import wraps
from hashlib import md5
from typing import Any, Callable, Optional

from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.trace import get_tracer
from redis.asyncio import Redis
from starlette.requests import Request
from starlette.responses import Response

from app.core.cache.redis_key_builder import (default_key_builder,
                                              request_key_builder,
                                              result_key_builder)
from app.core.configs.cache_config import cache_config
from app.core.constants import UTF_8
from app.core.data.data_response import DataResponse
from app.core.logs.logging_setup import get_logger
from app.core.monitoring.tracing import single_span, header_trace_key
from app.core.utils.dict_util import to_dict

KEY_PAYLOAD = "value"

_config = cache_config()
logger = get_logger(__name__)
tracer = get_tracer(__name__)

RedisInstrumentor().instrument()


class Cache:
    instance: Redis

    @classmethod
    async def init(cls):
        cls.instance = Redis(
            host=_config.redis_host,
            port=_config.redis_port,
            username=_config.username,
            password=_config.password,
            ssl=_config.use_ssl,
            decode_responses=True
        )
        await cls.instance.ping()


def redis() -> Redis:
    return Cache.instance


async def init():
    logger.info("Initializing redis cache...")

    await Cache.init()

    logger.info("Redis cache initialized!")


async def close():
    logger.info("Closing redis cache...")

    await redis().close()

    logger.info("Redis cache closed!")


async def health():
    try:
        pong = await redis().ping()

        return "UP" if pong else "DOWN"
    except:
        return "DOWN"


def cache_get(
        namespace: str,
        identifier="id",
        key_builder=request_key_builder
):
    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            request = kwargs.get("request")
            response = kwargs.get("response")
            key = get_key(
                func=func,
                namespace=namespace,
                identifier=identifier,
                args=args,
                kwargs=kwargs,
                key_builder=key_builder
            )
            result = await get(key)

            if result:
                if response:
                    ttl = await time_to_live(key)

                    with_headers(result, ttl, request, response)

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
        identifier="id",
        key_builder=result_key_builder,
        publish=False
):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            request = kwargs.get("request")
            result = await func(*args, **kwargs)

            if is_no_store(request):
                return result

            key = get_key(
                func=func,
                namespace=namespace,
                identifier=identifier,
                result=result,
                args=args,
                kwargs=kwargs,
                key_builder=key_builder
            )

            await set(key, result, publish)

            return result

        return inner

    return wrapper


def cache_evict(
        namespace: str,
        identifier="id",
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


def with_headers(result, ttl, request: Request, response: Response):
    dump = json.dumps(result, sort_keys=True).encode(UTF_8)
    etag = md5(dump).hexdigest()
    response.headers["Cache-Control"] = f"max-age={ttl}"
    response.headers["ETag"] = etag

    if not request:
        return

    if_none_match = request.headers.get("if-none-match")

    if if_none_match == etag:
        response.status_code = 304


def is_no_store(request: Request):
    return request and request.headers.get("Cache-Control") == "no-store"


async def set(key: str, value: Any, publish=False):
    value = serializer(value)

    with tracer.start_span(name="SET"):
        await redis().set(key, value, _config.ttl)

    if publish:
        with tracer.start_span(name="PUBLISH"):
            await redis().publish(key, value)


async def get(key: str):
    with tracer.start_span(name="GET"):
        value = await redis().get(key)

        return deserializer(value) if value else None


async def time_to_live(key: str):
    with tracer.start_span(name="TTL"):
        return await redis().ttl(key)


async def delete(*keys: str):
    with tracer.start_span(name="DEL"):
        await redis().delete(*keys)


def serializer(value: Any) -> Any:
    data = {
        KEY_PAYLOAD: to_dict(value),
        header_trace_key: single_span()
    }

    return json.dumps(data)


def deserializer(value: str) -> Any:
    data = json.loads(value)

    return data[KEY_PAYLOAD]
