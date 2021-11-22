from functools import lru_cache

from pydantic import BaseSettings


class AppConfig(BaseSettings):
    prefix = '/sample'
    port = 443
    workers = 1
    environment: str = 'local'
    language_default: str = 'en'
    internationalization_path: str = 'app/core/libraries/i18n/'
    message_path: str = 'app/core/libraries/messages/'

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def app_config():
    return AppConfig()
