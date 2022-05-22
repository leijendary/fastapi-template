from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.core.data.error_source import ErrorSource
from app.core.monitoring.tracing import get_trace_id


class ErrorResponse(JSONResponse):
    def render(self, errors: List[ErrorSource], meta=None) -> bytes:
        if meta is None:
            meta = {}

        trace_id = get_trace_id()

        if trace_id:
            meta["trace_id"] = trace_id

        content = {
            "errors": errors,
            "meta": {
                "status": self.status_code,
                "timestamp": datetime.utcnow(),
                **meta
            }
        }

        return super().render(jsonable_encoder(content))
