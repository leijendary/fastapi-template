from typing import Union

from jose import jwt
from starlette.requests import HTTPConnection, Request
from starlette_context.plugins.base import Plugin


class AuthorizationPlugin(Plugin):
    key = 'Authorization'

    async def process_request(self, request: Union[Request, HTTPConnection]):
        authorization = await super().extract_value_from_header_by_key(request)
        scheme, token = authorization.split()

        if scheme.lower() != 'bearer':
            return

        claims = jwt.get_unverified_claims(token)

        return claims['sub']
