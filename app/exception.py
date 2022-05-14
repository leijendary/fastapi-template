from botocore.exceptions import ClientError
from elasticsearch.exceptions import NotFoundError as SearchNotFoundError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose.exceptions import ExpiredSignatureError
from pydantic.error_wrappers import ValidationError
from tortoise.exceptions import IntegrityError

from app.core.errors.access_denied_error import access_denied_handler
from app.core.errors.client_error import client_error_handler
from app.core.errors.expired_token_error import expired_token_handler
from app.core.errors.generic_error import generic_handler
from app.core.errors.integrity_error import integrity_handler
from app.core.errors.invalid_token_error import invalid_token_handler
from app.core.errors.method_not_allowed_error import method_not_allowed_handler
from app.core.errors.not_found_error import not_found_handler
from app.core.errors.resource_not_found_error import resource_not_found_handler
from app.core.errors.search_not_found_error import search_not_found_handler
from app.core.errors.unauthorized_error import unauthorized_handler
from app.core.errors.validation_error import validation_handler
from app.core.exceptions.access_denied_exception import AccessDeniedException
from app.core.exceptions.invalid_token_exception import InvalidTokenException
from app.core.exceptions.resource_not_found_exception import \
    ResourceNotFoundException
from app.core.exceptions.unauthorized_exception import UnauthorizedException

functions = {
    404: not_found_handler,
    405: method_not_allowed_handler,
    InvalidTokenException: invalid_token_handler,
    UnauthorizedException: unauthorized_handler,
    ExpiredSignatureError: expired_token_handler,
    AccessDeniedException: access_denied_handler,
    ResourceNotFoundException: resource_not_found_handler,
    SearchNotFoundError: search_not_found_handler,
    IntegrityError: integrity_handler,
    RequestValidationError: validation_handler,
    ValidationError: validation_handler,
    ClientError: client_error_handler,
    Exception: generic_handler
}


def add_handlers(app: FastAPI):
    [app.add_exception_handler(key, value) for key, value in functions.items()]
