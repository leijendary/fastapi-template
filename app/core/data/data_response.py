from datetime import datetime
from typing import Generic, TypeVar

from app.core.data.schema import ResponseMetaSchema
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page
from pydantic import BaseModel
from pydantic.fields import Field

T = TypeVar('T')


class DataResponse(BaseModel, Generic[T]):
    data: T
    meta: ResponseMetaSchema = Field(...)

    def __init__(self, data: T, status=200, meta={}, **others) -> None:
        if isinstance(data, Page):
            meta = self.page_meta(data, meta)

            data = data.items

        meta = {
            'status': status,
            'timestamp': jsonable_encoder(datetime.utcnow()),
            **meta
        }

        super().__init__(data=data, meta=meta, **others)

    def page_meta(self, data: T, meta={}):
        return {
            **meta,
            'count': len(data.items),
            'total': data.total,
            'page': data.page,
            'size': data.size
        }
