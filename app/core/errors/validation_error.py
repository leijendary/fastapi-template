from typing import Dict

from pydantic import ValidationError

from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource


async def validation_handler(_, exc: ValidationError) -> ErrorResponse:
    sources = list(map(mapper, exc.errors()))

    return ErrorResponse(sources, 422)


def mapper(error: Dict[str, object]):
    sources = list(error["loc"])
    code = error["type"]
    message = error["msg"]

    return ErrorSource(sources=sources, code=code, message=message)
