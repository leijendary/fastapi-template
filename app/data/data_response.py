from datetime import datetime
from typing import Generic, TypeVar

from app.utils.date import to_epoch
from pydantic import BaseModel

T = TypeVar('T')


class DataResponse(BaseModel, Generic[T]):
    data: T
    meta: dict = {}

    def __init__(self, data: T, status=200, meta={}, **others) -> None:
        meta = {
            'status': status,
            'timestamp': datetime.utcnow(),
            **meta
        }

        super().__init__(data=data, meta=meta, **others)
