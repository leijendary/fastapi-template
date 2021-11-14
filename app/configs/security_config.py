from functools import lru_cache

from pydantic import BaseSettings


class SecurityConfig(BaseSettings):
    jwks_url: str
    jwks_cache_key = 'fastapi:jwks'
    audience: str
    token_url = ''
    scopes = ''

    class Config:
        env_prefix = 'security_'
        env_file = '.env'


@lru_cache
def security_config():
    return SecurityConfig()
