import re

from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message
from asyncpg.exceptions import UniqueViolationError
from starlette.responses import JSONResponse
from tortoise.exceptions import IntegrityError


async def integrity_handler(_, exc: IntegrityError) -> JSONResponse:
    cause = exc.args[0]

    if isinstance(cause, UniqueViolationError):
        return await unique_violation_handler(_, cause)

    sources = ['body', 'model']
    code = 'error.data_integrity'
    message = get_message(code, cause.detail)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 500
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)


async def unique_violation_handler(
    _,
    exc: UniqueViolationError
) -> JSONResponse:
    detail = exc.detail
    field = re.search('Key \((.+?)\)=', detail).group(1)
    value = re.search('=\((.+?)\)', detail).group(1)
    sources = ['body', exc.table_name, field]
    code = 'validation.already_exists'
    message = get_message(code, field, value)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = 409
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)
