from datetime import datetime
from typing import Any, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.monitoring.tracing import trace_id

T = TypeVar("T")


class DataResponse(JSONResponse):
    def render(self, data: Any, meta=None) -> bytes:
        if meta is None:
            meta = {"type": "object"}

        if data and {"items", "total", "page", "size"} <= set(data):
            meta = page_meta(data, meta)
            data = data["items"]

        if data and {"content", "size", "limit", "next_token"} <= set(data):
            meta = seek_meta(data, meta)
            data = data["content"]

        if isinstance(data, list):
            meta["type"] = "array"

        t_id = trace_id()

        if t_id:
            meta["trace_id"] = t_id

        content = {
            "data": data,
            "meta": {
                "status": self.status_code,
                "timestamp": datetime.utcnow(),
                **meta
            }
        }

        return super().render(jsonable_encoder(content))


def page_meta(data: T, meta=None):
    if meta is None:
        meta = {}

    return {
        **meta,
        "count": len(data["items"]),
        "total": data["total"],
        "page": data["page"],
        "size": data["size"]
    }


def seek_meta(data: T, meta=None):
    if meta is None:
        meta = {}

    return {
        **meta,
        "size": data["size"],
        "limit": data["limit"],
        "next_token": data["next_token"],
    }
