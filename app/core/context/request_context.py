from typing import Any

from app.configs.security_config import security_config
from app.core.plugins.request_plugin import AuthorizationPlugin
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError

_config = security_config()
_anonymous_user = _config.anonymous_user


def current_user():
    return get_context_value(AuthorizationPlugin.key, _anonymous_user)


def get_context_value(key: str, default: Any):
    try:
        return context.get(key, default)
    except ContextDoesNotExistError:
        return default
