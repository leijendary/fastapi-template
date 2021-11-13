from app.clients import jwks_client
from app.core.exceptions.invalid_token_exception import InvalidTokenException
from app.core.security.schemes import oauth2_scheme
from fastapi import Depends
from fastapi.security import SecurityScopes
from jose import jwk, jwt
from jose.utils import base64url_decode


async def check_scope(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):
    security_scopes.scopes
    header = jwt.get_unverified_header(token)
    kid = header.get('kid')
    message, encoded_signature = token.rsplit('.', 1)
    keys = await jwks_client.keys()

    for k in keys:
        if k['kid'] == kid:
            key = jwk.construct(k)

            break

    if not key:
        raise InvalidTokenException('Key not found in JWKs')

    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    if not key.verify(message.encode('utf-8'), decoded_signature):
        raise InvalidTokenException('Invalid token signature')
