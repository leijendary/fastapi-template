from functools import lru_cache

from pydantic import BaseSettings


class AppConfig(BaseSettings):
    port: int = 80
    environment: str = 'local'
    language_default: str = 'en'
    internationalization_path: str = 'app/resources/languages/i18n/'
    message_path: str = 'app/resources/messages/libraries/'

    class Config:
        env_prefix = ''
        env_file = '.env'


@lru_cache
def app_config():
    return AppConfig()
