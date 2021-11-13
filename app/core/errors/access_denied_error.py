from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message
from starlette.responses import JSONResponse


async def access_denied_handler(_, __) -> JSONResponse:
    sources = ['header', 'Authorization', 'scope']
    code = 'access.denied'
    message = get_message(code)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 403
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
