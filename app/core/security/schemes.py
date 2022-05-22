from fastapi import Request, WebSocket
from fastapi.security import OAuth2PasswordBearer

from app.core.configs.security_config import security_config

_config = security_config()

_scopes = {
    scope: ""
    for scope in _config.scopes.split(",")
}


class AppOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(
            self,
            request: Request = None,
            websocket: WebSocket = None
    ):
        return await super().__call__(request or websocket)


oauth2_scheme = AppOAuth2PasswordBearer(
    _config.token_url,
    "Bearer",
    _scopes,
    auto_error=False
)
