from app.configs.security_config import security_config
from fastapi.security import OAuth2PasswordBearer

_security_config = security_config()
token_url = _security_config.token_url

scopes = {
    scope: ''
    for scope in _security_config.scopes.split(',')
}

oauth2_scheme = OAuth2PasswordBearer(
    token_url,
    'Bearer',
    scopes,
    auto_error=False
)
