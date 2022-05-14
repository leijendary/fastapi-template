from app.core.configs.security_config import security_config
from app.core.exceptions.access_denied_exception import AccessDeniedException
from app.core.security.token_validator import token_claims
from fastapi import Depends
from fastapi.security import SecurityScopes

_config = security_config()
_sources = ["header", "x-scope"] if _config.use_scope_header else ["scope",
                                                                   "Authorization", "scope"]


async def check_scope(security_scopes: SecurityScopes, claims=Depends(token_claims)):
    scopes = security_scopes.scopes

    validate_scope(scopes, claims)


def validate_scope(scopes, claims):
    scope = claims["scope"] if "scope" in claims else None

    if not scope:
        raise AccessDeniedException("No scope provided", sources=_sources)

    if not any(scope in claims["scope"].split(" ") for scope in scopes):
        raise AccessDeniedException(
            "Scope not in any of the scopes",
            scopes,
            _sources
        )
