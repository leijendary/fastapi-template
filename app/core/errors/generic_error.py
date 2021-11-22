from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message
from starlette.responses import JSONResponse


async def generic_handler(_, exc: Exception) -> JSONResponse:
    reason = exc.args[0]
    sources = ['Generic']
    code = 'error.generic'
    message = get_message(code, reason)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 500
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
