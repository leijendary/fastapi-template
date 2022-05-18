from typing import Optional

from fastapi import Query
from fastapi_pagination.default import Params
from pydantic.main import BaseModel


class PageParams(Params):
    size: int = Query(10, ge=1, le=100, description="Page size")


class LimitParams(BaseModel):
    limit: int = Query(10, ge=1, le=100, description="Page limit")


class SeekParams(LimitParams):
    next_token: Optional[str] = Query(
        None,
        description="Token to identify the next set of rows to return"
    )


class SortParams(PageParams):
    sort: str = Query(
        None,
        description="Sort fields and direction",
        example="-created_at,-_score,first_name"
    )
