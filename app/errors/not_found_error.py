from app.data.error_response import ErrorResponse
from app.data.error_source import ErrorSource
from app.resources.messages.message import get_message
from starlette.requests import Request


async def not_found_handler(request: Request, _) -> ErrorResponse:
    sources = ['path']
    code = 'error.mapping_not_found'
    path = request.url.path
    query = request.url.query

    if query:
        path += '?' + query

    message = get_message(code, path)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 404)
