from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message
from elasticsearch.exceptions import NotFoundError
from starlette.responses import JSONResponse


async def search_not_found_handler(_, exc: NotFoundError) -> JSONResponse:
    resource = exc.info['_index']
    identifier = exc.info['_id']
    sources = ['search', resource, identifier]
    code = 'error.search_not_found'
    message = get_message(code, resource, identifier)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = exc.status_code
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
