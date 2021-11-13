from typing import Dict

from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from pydantic import ValidationError
from starlette.responses import JSONResponse


async def validation_handler(_, exc: ValidationError) -> JSONResponse:
    sources = list(map(mapper, exc.errors()))
    status_code = 422
    response = ErrorResponse(sources, status_code)

    return JSONResponse(response.dict(), status_code)


def mapper(error: Dict[str, object]):
    sources = list(error['loc'])
    code = error['type']
    message = error['msg']

    return ErrorSource(sources=sources, code=code, message=message)
