import time
from typing import List

from app.data.error_source import ErrorSource
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
            'timestamp': time.time_ns() // 100000,
            **meta
        }

        super().__init__(errors=errors, meta=meta, **others)
