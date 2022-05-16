from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from .error_source import ErrorSource
from ..monitoring.tracing import trace_id


class ErrorResponse(JSONResponse):
    def render(self, errors: List[ErrorSource], meta=None) -> bytes:
        if meta is None:
            meta = {}

        t_id = trace_id()

        if t_id:
            meta["trace_id"] = t_id

        content = {
            "errors": errors,
            "meta": {
                "status": self.status_code,
                "timestamp": datetime.utcnow(),
                **meta
            }
        }

        return super().render(jsonable_encoder(content))
