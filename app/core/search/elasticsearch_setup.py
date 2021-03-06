import logging
from typing import Dict, Optional, Mapping, Any, Union

from elasticsearch import AsyncElasticsearch, AsyncTransport
from opentelemetry.trace import get_tracer, SpanKind

from app.core.configs.elasticsearch_config import elasticsearch_config
from app.core.logs.logging_setup import get_logger

_config = elasticsearch_config()
logger = get_logger(__name__)
tracer = get_tracer(__name__)

# Override elasticsearch log level
_logger = logging.getLogger("elasticsearch")
_logger.setLevel(_config.log_level)


class OpenTelemetryAsyncTransport(AsyncTransport):
    span_kind = SpanKind.CLIENT

    async def perform_request(
            self,
            method: str,
            url: str,
            headers: Optional[Mapping[str, str]] = ...,
            params: Optional[Mapping[str, Any]] = ...,
            body: Optional[Any] = ...,
    ) -> Union[bool, Any]:
        if isinstance(body, type(Ellipsis)):
            body = None

        name = f"{method} {url}"

        with tracer.start_span(name, kind=self.span_kind):
            return await super().perform_request(
                method,
                url,
                headers,
                params,
                body
            )


class Elasticsearch:
    instance: AsyncElasticsearch

    @classmethod
    def init(cls):
        scheme = "https" if _config.use_ssl else "http"
        http_auth = (
            (_config.username, _config.password)
            if _config.username and _config.password else None
        )

        cls.instance = AsyncElasticsearch(
            hosts=_config.hosts.split(","),
            scheme=scheme,
            use_ssl=_config.use_ssl,
            http_auth=http_auth,
            transport_class=OpenTelemetryAsyncTransport
        )


def elasticsearch() -> AsyncElasticsearch:
    return Elasticsearch.instance


def init():
    logger.info("Initializing elasticsearch...")

    Elasticsearch.init()

    logger.info("Elasticsearch initialized!")


async def create_index(index: str, body: Dict):
    client = elasticsearch().indices

    if await client.exists(index=index):
        logger.info(f"Updating index for {index}...")

        await client.put_mapping(body=body["mappings"], index=index)

        logger.info(f"Updated index for {index}!")
    else:
        logger.info(f"Creating index for {index}...")

        await client.create(index=index, body=body)

        logger.info(f"Created index for {index}!")


async def close():
    logger.info("Closing elasticsearch...")

    await elasticsearch().close()

    logger.info("Elasticsearch closed!")


async def health():
    try:
        info = await elasticsearch().info()

        return "UP" if info else "DOWN"
    except:
        return "DOWN"
