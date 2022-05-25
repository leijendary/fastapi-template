import re

from asyncpg.exceptions import UniqueViolationError
from tortoise.exceptions import IntegrityError

from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message


async def integrity_handler(_, exc: IntegrityError) -> ErrorResponse:
    cause = exc.args[0]

    if isinstance(cause, UniqueViolationError):
        return await unique_violation_handler(_, cause)

    sources = ["body", "model"]
    code = "error.data_integrity"
    message = get_message(code, cause.message)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 500)


async def unique_violation_handler(
        _,
        exc: UniqueViolationError
) -> ErrorResponse:
    detail = exc.detail
    field = re.search("Key \((.+?)\)=", detail).group(1)

    if "::" in field:
        field = re.search("\((.+?)::", field).group(1)

    value = re.search("=\((.+?)\)", detail).group(1)
    sources = ["body", exc.table_name, field]
    code = "validation.already_exists"
    message = get_message(code, field, value)
    source = ErrorSource(sources=sources, code=code, message=message)

    return ErrorResponse([source], 409)
