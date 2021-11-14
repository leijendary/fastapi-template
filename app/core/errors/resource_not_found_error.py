from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.exceptions.resource_not_found_exception import \
    ResourceNotFoundException
from app.core.libraries.message import get_message
from starlette.responses import JSONResponse


async def resource_not_found_handler(
    _,
    exc: ResourceNotFoundException
) -> JSONResponse:
    resource = exc.resource
    identifier = exc.identifier
    sources = ['model', resource, identifier]
    code = 'error.resource_not_found'
    message = get_message(code, resource, identifier)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 404
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
