from starlette.requests import Request
from tortoise.exceptions import DoesNotExist

from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message


async def does_not_exist_handler(
        request: Request,
        _: DoesNotExist
) -> ErrorResponse:
    path = request.url.path
    sources = path.split("/")[1:-1]
    code = "error.does_not_exist"
    message = get_message(code, path)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 404)
