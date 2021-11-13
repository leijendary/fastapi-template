from datetime import datetime
from typing import List

from app.data.error_source import ErrorSource
from fastapi.encoders import jsonable_encoder
from pydantic.main import BaseModel


class ErrorResponse(BaseModel):
    errors: List[ErrorSource] = []
    meta: dict = {}

    def __init__(
        self,
        errors: List[ErrorSource] = [],
        status=500,
        meta={},
        **others
    ) -> None:
        meta = {
            'status': status,
            'timestamp': jsonable_encoder(datetime.utcnow()),
            **meta
        }

        super().__init__(errors=errors, meta=meta, **others)
