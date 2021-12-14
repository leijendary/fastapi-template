from app.core.data.error_response import ErrorResponse, ErrorSource
from app.core.libraries.message import get_message


async def unauthorized_handler(_, __) -> ErrorResponse:
    sources = ["header", "Authorization"]
    code = "access.unauthorized"
    message = get_message(code)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 401)
