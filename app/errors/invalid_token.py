from app.data.error_response import ErrorResponse, ErrorSource
from app.errors.exceptions.invalid_token_exception import InvalidTokenException
from app.resources.messages.message import get_message


async def invalid_token_handler(
    _,
    exc: InvalidTokenException
) -> ErrorResponse:
    reason = exc.args[0]
    sources = ['Token']
    code = 'access.invalid'
    message = get_message(code, reason)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 400)
