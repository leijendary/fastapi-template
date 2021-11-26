from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message
from starlette.requests import Request
from starlette.responses import JSONResponse


async def method_not_allowed_handler(request: Request, _) -> JSONResponse:
    sources = ['method']
    code = 'error.method_not_supported'
    method = request.method

    message = get_message(code, method)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 405
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
