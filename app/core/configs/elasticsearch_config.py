from functools import lru_cache
from logging import WARNING
from typing import Optional

from pydantic import BaseSettings


class ElasticsearchConfig(BaseSettings):
    hosts: Optional[str]
    username: Optional[str]
    password: Optional[str]
    ca_certs = "ssl/elasticsearch.crt"
    log_level = WARNING

    class Config:
        env_prefix = "elasticsearch_"
        env_file = ".env"


@lru_cache
def elasticsearch_config() -> ElasticsearchConfig:
    return ElasticsearchConfig()
