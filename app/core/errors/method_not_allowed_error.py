from starlette.requests import Request

from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message


async def method_not_allowed_handler(request: Request, _) -> ErrorResponse:
    sources = ["method"]
    code = "error.method_not_supported"
    method = request.method

    message = get_message(code, method)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 405)
