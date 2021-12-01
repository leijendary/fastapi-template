from app.configs.security_config import security_config
from fastapi.security import OAuth2PasswordBearer

_config = security_config()

scopes = {
    scope: ''
    for scope in _config.scopes.split(',')
}

oauth2_scheme = OAuth2PasswordBearer(
    _config.token_url,
    'Bearer',
    scopes,
    auto_error=False
)
