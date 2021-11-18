from functools import lru_cache
from logging import WARNING
from typing import Optional

from pydantic import BaseSettings


class ElasticsearchConfig(BaseSettings):
    hosts: Optional[str]
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
