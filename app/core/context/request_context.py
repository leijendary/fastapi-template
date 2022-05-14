from typing import Any

from app.core.configs.app_config import app_config
from app.core.configs.security_config import security_config
from app.core.plugins.request_plugin import (AuthorizationPlugin,
                                             LanguagePlugin, UserPlugin)
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError

_app_config = app_config()
_language_default = _app_config.language_default
_security_config = security_config()
_anonymous_user = _security_config.anonymous_user
_use_user_header = _security_config.use_user_header


def current_user():
    key = UserPlugin.key if _use_user_header else AuthorizationPlugin.key

    return get_context_value(key, _anonymous_user)


def current_language():
    return get_context_value(LanguagePlugin.key, _language_default)


def get_context_value(key: str, default: Any):
    try:
        value = context.get(key, default)

        return value if value else default
    except ContextDoesNotExistError:
        return default
