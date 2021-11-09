from functools import lru_cache

from pydantic import BaseSettings


class KafkaConfig(BaseSettings):
    kafka_client_id: str
    kafka_group_id: str
    kafka_brokers: str

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def kafka_config():
    return KafkaConfig()
