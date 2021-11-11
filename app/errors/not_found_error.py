from app.data.error_response import ErrorResponse
from app.data.error_source import ErrorSource
from app.resources.messages.message import get_message
from starlette.requests import Request
from starlette.responses import JSONResponse


async def not_found_handler(request: Request, _):
    sources = ['path']
    code = 'error.mapping_not_found'
    path = request.url.path
    query = request.url.query

    if query:
        path += '?' + query

    message = get_message(code, path)
    error = ErrorSource(sources=sources, code=code, message=message)
    status_code = 404
    response = ErrorResponse([error], status_code)

    return JSONResponse(response.dict(), status_code)
