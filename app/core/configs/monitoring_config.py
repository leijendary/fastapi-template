from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class MonitoringConfig(BaseSettings):
    host: Optional[str]
    port: Optional[int]
    sample_rate = 1.0
    inject_response_headers = True
    force_new_trace = False

    class Config:
        env_prefix = "monitoring_"
        env_file = ".env"


@lru_cache
def monitoring_config():
    return MonitoringConfig()
