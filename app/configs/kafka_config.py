from functools import lru_cache

from pydantic import BaseSettings


class KafkaConfig(BaseSettings):
    client_id: str
    group_id: str
    brokers: str

    class Config:
        env_prefix = 'kafka_'
        env_file = '.env'


@lru_cache
def kafka_config():
    return KafkaConfig()
