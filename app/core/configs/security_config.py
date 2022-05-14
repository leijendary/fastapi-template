from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class SecurityConfig(BaseSettings):
    # Whether to use the X-Scope header
    use_scope_header = True
    # Whether to use the X-User-ID header
    use_user_header = True
    jwks_url: Optional[str]
    jwks_cache_key = "fastapi:jwks"
    audience: Optional[str]
    token_url = ""
    scopes = ""
    ssl_certfile = "ssl/certificate.pem"
    ssl_keyfile = "ssl/key.pem"
    encryption_password: str
    encryption_salt: str
    anonymous_user = "Anonymous"

    class Config:
        env_prefix = "security_"
        env_file = ".env"


@lru_cache
def security_config() -> SecurityConfig:
    return SecurityConfig()
