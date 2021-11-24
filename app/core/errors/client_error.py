from app.core.data.error_response import ErrorResponse
from app.core.data.error_source import ErrorSource
from app.core.libraries.message import get_message
from app.core.utils.file_util import get_name
from botocore.exceptions import ClientError
from starlette.responses import JSONResponse


async def client_error_handler(_, exc: ClientError) -> JSONResponse:
    error = exc.response['Error']
    key = error['Key']
    sources = ['File']
    code = 'error.generic'
    reason = error['Message']

    if error['Code'] == 'NoSuchKey':
        name = get_name(key)
        code = 'error.file_not_found'
        reason = name

        sources.append(name)

    message = get_message(code, reason)
    source = ErrorSource(sources=sources, code=code, message=message)
    status_code = exc.response['ResponseMetadata']['HTTPStatusCode']
    response = ErrorResponse([source], status_code)

    return JSONResponse(response.dict(), status_code)