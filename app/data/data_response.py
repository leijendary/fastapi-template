import time
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class DataResponse(BaseModel, Generic[T]):
    data: T
    meta: dict = {}

    def __init__(self, data: T, status=200, meta={}, **others) -> None:
        meta = {
            'status': status,
            'timestamp': time.time_ns() // 100000,
            **meta
        }

        super().__init__(data=data, meta=meta, **others)
