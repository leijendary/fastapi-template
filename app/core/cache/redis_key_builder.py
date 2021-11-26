from typing import Any, Optional


def default_key_builder(
    func,
    namespace: str,
    identifier: Optional[str] = None,
    result: Optional[Any] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    return namespace


def request_key_builder(
    func,
    namespace: str,
    identifier: str,
    result: Optional[Any] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    value = kwargs[identifier]

    return f"{namespace}:{value}"


def result_key_builder(
    func,
    namespace: str,
    identifier: str,
    result: Any = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    value = getattr(result, identifier)

    return f"{namespace}:{value}"
