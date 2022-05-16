from typing import Any

from fastapi_pagination import create_page
from tortoise.queryset import QuerySet

from app.core.data.params import SortParams
from app.core.models.model import Model


async def to_page(query: QuerySet[Model], params: SortParams, type: Any):
    raw_params = params.to_raw_params()
    items = await (
        query
            .offset(raw_params.offset)
            .limit(raw_params.limit)
            .order_by(*params.sort.split(","))
            .all()
    )
    total = await query.count()
    records = [type(**item.dict()) for item in items]

    return create_page(records, total, params)
