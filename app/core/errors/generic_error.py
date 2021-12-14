from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message


async def generic_handler(_, exc: Exception) -> ErrorResponse:
    reason = exc.args[0]
    sources = ["Generic"]
    code = "error.generic"
    message = get_message(code, reason)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 500)
