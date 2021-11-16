from functools import lru_cache
from logging import WARNING

from pydantic import BaseSettings


class ElasticsearchConfig(BaseSettings):
    hosts: str
    log_level = WARNING
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
