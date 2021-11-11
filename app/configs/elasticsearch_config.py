import json
from functools import lru_cache

from app.configs.constants import INDEX_SAMPLE
from pydantic import BaseSettings

from elasticsearch import AsyncElasticsearch

indices = {
    INDEX_SAMPLE: {
        'settings': json.load(open('app/configs/elasticsearch/ngram-analyzer.settings.json')),
        'mappings': json.load(open('app/configs/elasticsearch/sample.mapping.json'))
    }
}


class ElasticsearchConfig(BaseSettings):
    elasticsearch_hosts: str
    elasticsearch_use_ssl = False
    elasticsearch_verify_certs = False
    elasticsearch_ca_certs: str = None
    elasticsearch_client_cert: str = None
    elasticsearch_client_key: str = None

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def elasticsearch_config():
    return ElasticsearchConfig()


config = elasticsearch_config()
elasticsearch = AsyncElasticsearch(
    hosts=config.elasticsearch_hosts.split(','),
    use_ssl=config.elasticsearch_use_ssl,
    verify_certs=config.elasticsearch_verify_certs,
    ca_certs=config.elasticsearch_ca_certs,
    client_cert=config.elasticsearch_client_cert,
    client_key=config.elasticsearch_client_key
)


async def init():
    for index, body in indices.items():
        if not await elasticsearch.indices.exists(index):
            await elasticsearch.indices.create(index, body)
