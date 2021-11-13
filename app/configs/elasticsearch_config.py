import json
from functools import lru_cache

from app.configs.constants import INDEX_SAMPLE
from app.configs.logging_config import get_logger
from pydantic import BaseSettings

from elasticsearch import AsyncElasticsearch

logger = get_logger(__name__)

indices = {
    INDEX_SAMPLE: {
        'settings': json.load(open('app/configs/elasticsearch/ngram-analyzer.settings.json')),
        'mappings': json.load(open('app/configs/elasticsearch/sample.mapping.json'))
    }
}


class ElasticsearchConfig(BaseSettings):
    hosts: str
    use_ssl = False
    verify_certs = False
    ca_certs: str = None
    client_cert: str = None
    client_key: str = None

    class Config:
        env_prefix = 'elasticsearch_'
        env_file = '.env'


@lru_cache
def elasticsearch_config():
    return ElasticsearchConfig()


config = elasticsearch_config()
elasticsearch = AsyncElasticsearch(
    hosts=config.hosts.split(','),
    use_ssl=config.use_ssl,
    verify_certs=config.verify_certs,
    ca_certs=config.ca_certs,
    client_cert=config.client_cert,
    client_key=config.client_key
)


async def init():
    logger.info('Initializing elasticsearch...')

    for index, body in indices.items():
        if await elasticsearch.indices.exists(index):
            await elasticsearch.indices.put_mapping(body['mappings'], index)
        else:
            await elasticsearch.indices.create(index, body)

    logger.info('Elasticsearch initialized!')


async def close():
    logger.info('Closing elasticsearch...')

    await elasticsearch.close()

    logger.info('Elasticsearch closed!')
