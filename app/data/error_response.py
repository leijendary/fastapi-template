from datetime import datetime
from typing import List

from app.data.error_source import ErrorSource
from app.utils.date import to_epoch
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
            'timestamp': datetime.utcnow(),
            **meta
        }

        super().__init__(errors=errors, meta=meta, **others)
