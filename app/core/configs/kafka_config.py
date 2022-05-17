from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class KafkaConfig(BaseSettings):
    client_id: Optional[str]
    group_id: Optional[str]
    brokers: Optional[str]
    dlq_suffix = ".error"

    class Config:
        env_prefix = "kafka_"
        env_file = ".env"


@lru_cache
def kafka_config() -> KafkaConfig:
    return KafkaConfig()
