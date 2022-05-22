from datetime import datetime
from typing import Any, TypeVar, Tuple, Optional, Dict

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.monitoring.tracing import get_trace_id

T = TypeVar("T")


class DataResponse(JSONResponse):
    def render(self, data: Any, meta=None) -> bytes:
        data, meta = parse(data, meta)

        if isinstance(data, list):
            meta["type"] = "array"

        trace_id = get_trace_id()

        if trace_id:
            meta["trace_id"] = trace_id

        content = {
            "data": data,
            "meta": {
                "status": self.status_code,
                "timestamp": datetime.utcnow(),
                **meta
            }
        }

        return super().render(jsonable_encoder(content))


def parse(data: T, meta: Optional[Dict]) -> Tuple[T, Any]:
    if meta is None:
        meta = {"type": "object"}

    if data and {"items", "total", "page", "size"} <= set(data):
        meta = page_meta(data, meta)
        data = data["items"]

        return data, meta

    if data and {"content", "size", "limit", "next_token"} <= set(data):
        meta = seek_meta(data, meta)
        data = data["content"]

        return data, meta

    return data, meta


def page_meta(data: T, meta: Dict):
    return {
        **meta,
        "count": len(data["items"]),
        "total": data["total"],
        "page": data["page"],
        "size": data["size"]
    }


def seek_meta(data: T, meta: Dict):
    return {
        **meta,
        "size": data["size"],
        "limit": data["limit"],
        "next_token": data["next_token"],
    }
