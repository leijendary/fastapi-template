from typing import List

from app.clients import jwks_client
from app.core.exceptions.access_denied_exception import AccessDeniedException
from app.core.exceptions.invalid_token_exception import InvalidTokenException
from app.core.exceptions.unauthorized_exception import UnauthorizedException
from app.core.security.schemes import oauth2_scheme
from fastapi import Depends
from fastapi.security import SecurityScopes
from jose import jwk, jwt
from jose.utils import base64url_decode


async def check_scope(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):
    if not token:
        raise UnauthorizedException('No token provided')

    scopes = security_scopes.scopes

    await validate_key(token)

    result = has_any_scope(scopes, token)

    if not result:
        raise AccessDeniedException('Scope not in any of the scopes', scopes)


async def get_key(kid: str) -> str:
    keys = await jwks_client.keys()

    for k in keys:
        if k['kid'] == kid:
            key = jwk.construct(k)

            break

    if not key:
        raise InvalidTokenException('Key not found in JWKs')

    return key


async def validate_key(token: str):
    header = jwt.get_unverified_header(token)
    kid = header.get('kid')
    key = await get_key(kid)
    message, signature = token.rsplit('.', 1)
    decoded_signature = base64url_decode(signature.encode('utf-8'))

    if not key.verify(message.encode('utf-8'), decoded_signature):
        raise InvalidTokenException('Invalid token signature')


def has_any_scope(scopes: List[str], token: str) -> bool:
    claims = jwt.get_unverified_claims(token)

    return any(scope in claims['scope'].split(' ') for scope in scopes)
