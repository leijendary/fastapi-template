from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class SecurityConfig(BaseSettings):
    jwks_url: Optional[str]
    jwks_cache_key = 'fastapi:jwks'
    audience: Optional[str]
    token_url = ''
    scopes = ''
    ssl_certfile = 'ssl/certificate.pem'
    ssl_keyfile = 'ssl/key.pem'

    class Config:
        env_prefix = 'security_'
        env_file = '.env'


@lru_cache
def security_config():
    return SecurityConfig()
