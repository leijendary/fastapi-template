from typing import List

from app.core.configs.security_config import security_config
from app.core.exceptions.access_denied_exception import AccessDeniedException
from app.core.security.token_validator import token_claims
from fastapi import Depends
from fastapi.security import SecurityScopes

_config = security_config()
_sources: List[str]

if _config.use_scope_header:
    _sources = ["header", "x-scope"]
else:
    _sources = ["header", "Authorization", "scope"]


async def check_scope(
    security_scopes: SecurityScopes,
    claims=Depends(token_claims)
):
    scopes = security_scopes.scopes

    validate_scope(scopes, claims)


def validate_scope(scopes, claims):
    scope = claims["scope"] if "scope" in claims else None

    if not scope:
        raise AccessDeniedException("No scope provided", sources=_sources)

    split = scope.split(" ")

    if not any(s in split for s in scopes):
        raise AccessDeniedException(
            "Scope not in any of the scopes",
            scopes,
            _sources
        )
