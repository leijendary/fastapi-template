from fastapi import Query
from fastapi_pagination.default import Params


class PageParams(Params):
    size: int = Query(10, ge=1, le=100, description='Page size')


class SortParams(PageParams):
    sort: str = Query(
        None,
        description='Sort fields and direction',
        example='-created_at,-_score,first_name'
    )
