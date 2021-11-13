from app.core.data.error_response import ErrorResponse, ErrorSource
from app.core.libraries.message import get_message
from starlette.responses import JSONResponse


async def invalid_token_handler(_, __) -> JSONResponse:
    sources = ['header', 'Authorization']
    code = 'access.invalid'
    message = get_message(code)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 401
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
