from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class ClientConfig(BaseSettings):
    sample_url: Optional[str]

    class Config:
        env_prefix = "client_"
        env_file = ".env"


@lru_cache
def client_config():
    return ClientConfig()
