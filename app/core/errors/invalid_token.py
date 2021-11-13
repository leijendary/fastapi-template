from app.core.data.error_response import ErrorResponse, ErrorSource
from app.core.exceptions.invalid_token_exception import InvalidTokenException
from app.core.libraries.message import get_message
from starlette.responses import JSONResponse


async def invalid_token_handler(_, exc: InvalidTokenException) -> JSONResponse:
    reason = exc.args[0]
    sources = ['Token']
    code = 'access.invalid'
    message = get_message(code, reason)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 400
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
