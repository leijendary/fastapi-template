from app.core.exceptions.access_denied_exception import AccessDeniedException
from app.core.security.token_validator import check_token
from fastapi import Depends
from fastapi.security import SecurityScopes


async def check_scope(
    security_scopes: SecurityScopes,
    claims=Depends(check_token)
):
    scopes = security_scopes.scopes

    validate_scope(scopes, claims)


def validate_scope(scopes, claims):
    if "scope" not in claims:
        raise AccessDeniedException("No scope provided")

    if not any(scope in claims["scope"].split(" ") for scope in scopes):
        raise AccessDeniedException("Scope not in any of the scopes", scopes)
