import logging
from typing import Dict

from elasticsearch import AsyncElasticsearch

from app.core.configs.elasticsearch_config import elasticsearch_config
from app.core.logs.logging_setup import get_logger

_config = elasticsearch_config()
logger = get_logger(__name__)

# Override elasticsearch log level
tracer = logging.getLogger("elasticsearch")
tracer.setLevel(_config.log_level)


class Elasticsearch:
    instance: AsyncElasticsearch

    @classmethod
    def init(cls):
        cls.instance = AsyncElasticsearch(
            hosts=_config.hosts.split(","),
            use_ssl=_config.use_ssl,
            verify_certs=_config.verify_certs,
            ca_certs=_config.ca_certs,
            client_cert=_config.client_cert,
            client_key=_config.client_key
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
