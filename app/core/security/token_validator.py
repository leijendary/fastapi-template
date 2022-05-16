from calendar import timegm
from datetime import datetime

from fastapi import Header
from fastapi.param_functions import Depends
from jose import jwk, jwt
from jose.exceptions import ExpiredSignatureError
from jose.utils import base64url_decode

from app.core.clients import jwks_client
from app.core.configs.security_config import security_config
from app.core.exceptions.invalid_token_exception import InvalidTokenException
from app.core.exceptions.unauthorized_exception import UnauthorizedException
from app.core.security.schemes import oauth2_scheme

_config = security_config()
_use_scope_header = _config.use_scope_header


async def token_claims(
        token: str = Depends(oauth2_scheme),
        x_scope: str = Header(default=None)
):
    if _use_scope_header:
        return {"scope": x_scope}

    if not token:
        raise UnauthorizedException("No token provided")

    await validate_key(token)

    claims = jwt.get_unverified_claims(token)

    validate_expiry(claims["exp"])
    validate_audience(claims["aud"])

    return claims


async def get_key(kid: str) -> str:
    keys = await jwks_client.keys()

    for k in keys:
        if k["kid"] == kid:
            key = jwk.construct(k)

            break
    else:
        raise InvalidTokenException("Key not found in JWKs")

    return key


async def validate_key(token: str):
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    key = await get_key(kid)
    message, signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(signature.encode("utf-8"))

    if not key.verify(message.encode("utf-8"), decoded_signature):
        raise InvalidTokenException("Invalid token signature")


def validate_expiry(exp: int):
    now = timegm(datetime.utcnow().utctimetuple())

    if exp < now:
        raise ExpiredSignatureError("Signature expired")


def validate_audience(aud: str):
    if aud != _config.audience:
        raise UnauthorizedException("Invalid audience")
