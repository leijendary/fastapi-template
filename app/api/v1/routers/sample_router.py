from typing import List
from uuid import UUID

from app.api.v1.data.sample_in import SampleIn
from app.api.v1.data.sample_out import SampleOut
from app.api.v1.data.sample_search_out import SampleSearchOut
from app.api.v1.search import sample_search
from app.api.v1.services import sample_service
from app.core.cache.redis_cache import cache_evict, cache_get, cache_put
from app.core.data.data_response import DataResponse
from app.core.security.scope_validator import check_scope
from fastapi import APIRouter
from fastapi.param_functions import Header, Security
from fastapi_pagination.default import Page

router = APIRouter(
    prefix='/api/v1/samples',
    tags=['samples']
)


@router.get(
    path='/search/',
    response_model=DataResponse[Page[SampleSearchOut]],
    status_code=200
)
async def search_page(
    query,
    page=1,
    size=10,
    sort: List[str] = None,
    accept_language=Header(None)
):
    result = await sample_search.page(accept_language, query, page, size, sort)

    return DataResponse(result, 200)


@router.get(
    path='/{id}/',
    response_model=DataResponse[SampleOut],
    status_code=200,
    dependencies=[
        Security(check_scope, scopes=['urn:sample:get:v1'])
    ]
)
@cache_get(namespace='sample:v1')
async def get(id: UUID):
    result = await sample_service.get(id)

    return DataResponse(result, 200)


@router.post(
    path='/',
    response_model=DataResponse[SampleOut],
    status_code=201,
    dependencies=[
        Security(check_scope, scopes=['urn:sample:create:v1'])
    ]
)
@cache_put(namespace='sample:v1')
async def save(sample_in: SampleIn):
    result = await sample_service.save(sample_in)

    return DataResponse(result, 201)


@router.delete(
    path='/{id}/',
    status_code=204,
    dependencies=[
        Security(check_scope, scopes=['urn:sample:delete:v1'])
    ]
)
@cache_evict(namespace='sample:v1')
async def delete(id: UUID):
    await sample_service.delete(id)
