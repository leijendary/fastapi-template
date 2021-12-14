from app.core.data.error_response import ErrorResponse, ErrorSource
from app.core.libraries.message import get_message


async def invalid_token_handler(_, __) -> ErrorResponse:
    sources = ["header", "Authorization"]
    code = "access.invalid"
    message = get_message(code)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 401)
