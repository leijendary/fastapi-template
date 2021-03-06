from functools import lru_cache

from pydantic import BaseSettings


class AppConfig(BaseSettings):
    name = "FastAPI Template"
    version = "0.0.1"
    prefix = ""
    port = 443
    workers = 1
    environment: str = "local"
    language_default: str = "en"
    internationalization_path: str = "resources/i18n/"
    message_path: str = "resources/messages/"

    class Config:
        env_prefix = ""
        env_file = ".env"


@lru_cache
def app_config() -> AppConfig:
    return AppConfig()
