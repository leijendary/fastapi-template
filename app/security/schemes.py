from app.configs.security_config import security_config
from fastapi.security import OAuth2PasswordBearer

config = security_config()
token_url = config.token_url
scopes = {
    scope: ''
    for scope in config.scopes.split(',')
}

oauth2_scheme = OAuth2PasswordBearer(token_url, 'Bearer', scopes)
