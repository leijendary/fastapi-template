import json
import logging

from app.configs.constants import INDEX_SAMPLE
from app.configs.elasticsearch_config import elasticsearch_config
from app.core.logs.logging import get_logger

from elasticsearch import AsyncElasticsearch

logger = get_logger(__name__)
_elasticsearch_config = elasticsearch_config()

# Override elasticsearch log level
tracer = logging.getLogger('elasticsearch')
tracer.setLevel(_elasticsearch_config.log_level)

indices = {
    INDEX_SAMPLE: {
        'settings': json.load(
            open('app/core/search/ngram-analyzer.settings.json')
        ),
        'mappings': json.load(
            open('app/core/search/sample.mapping.json')
        )
    }
}

elasticsearch = AsyncElasticsearch(
    hosts=_elasticsearch_config.hosts.split(','),
    use_ssl=_elasticsearch_config.use_ssl,
    verify_certs=_elasticsearch_config.verify_certs,
    ca_certs=_elasticsearch_config.ca_certs,
    client_cert=_elasticsearch_config.client_cert,
    client_key=_elasticsearch_config.client_key
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
