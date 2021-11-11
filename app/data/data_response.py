from datetime import datetime
from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

T = TypeVar('T')


class DataResponse(BaseModel, Generic[T]):
    data: T
    meta: dict = {}

    def __init__(self, data: T, status=200, meta={}, **others) -> None:
        meta = {
            'status': status,
            'timestamp': jsonable_encoder(datetime.utcnow()),
            **meta
        }

        super().__init__(data=data, meta=meta, **others)
