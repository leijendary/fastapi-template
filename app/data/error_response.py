from datetime import datetime
from typing import Any, List

from app.data.error_source import ErrorSource
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


class ErrorResponse(JSONResponse):
    errors: List[ErrorSource] = []
    meta: dict = {}

    def render(self, content: Any) -> bytes:
        meta = {
            'status': self.status_code,
            'timestamp': jsonable_encoder(datetime.utcnow()),
        }
        content = {
            'errors': jsonable_encoder(content),
            'meta': meta
        }

        return super().render(content)
