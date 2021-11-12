from app.data.error_response import ErrorResponse
from app.data.error_source import ErrorSource
from app.resources.messages.message import get_message
from tortoise.exceptions import DoesNotExist


async def not_exists_handler(_, exc: DoesNotExist) -> ErrorResponse:
    sources = ['model']
    code = 'error.resource_not_found'
    message = get_message(code, exc.detail)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 404)
