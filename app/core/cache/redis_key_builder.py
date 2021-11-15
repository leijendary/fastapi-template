from typing import Optional

from app.core.data.data_response import DataResponse


def default_key_builder(
    func,
    namespace: str,
    identifier: Optional[str] = None,
    result: Optional[DataResponse] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    return namespace


def request_key_builder(
    func,
    namespace: str,
    identifier: str,
    result: Optional[DataResponse] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    value = kwargs[identifier]

    return f"{namespace}:{value}"


def result_key_builder(
    func,
    namespace: str,
    identifier: str,
    result: DataResponse = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    value = getattr(result.data, identifier)

    return f"{namespace}:{value}"
