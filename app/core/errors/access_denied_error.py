from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.exceptions.access_denied_exception import AccessDeniedException
from app.core.libraries.message import get_message


async def access_denied_handler(
        _,
        exc: AccessDeniedException
) -> ErrorResponse:
    code = "access.denied"
    message = get_message(code)
    source = ErrorSource(sources=exc.sources, code=code, message=message)

    return ErrorResponse([source], 403)
