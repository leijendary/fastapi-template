from app.data.error_response import ErrorResponse
from app.data.error_source import ErrorSource
from app.resources.messages.message import get_message
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist


async def not_exists_handler(_, exc: DoesNotExist) -> JSONResponse:
    sources = ['model']
    code = 'error.resource_not_found'
    message = get_message(code, exc.detail)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 404
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
