from functools import lru_cache

from pydantic import BaseSettings


class AppConfig(BaseSettings):
    port: int = 443
    environment: str = 'local'
    workers = 1
    access_log = False
    use_colors = False
    language_default: str = 'en'
    internationalization_path: str = 'app/core/libraries/i18n/'
    message_path: str = 'app/core/libraries/messages/'

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def app_config():
    return AppConfig()
