from typing import List

from app.api.v1.data.sample_in import SampleIn
from app.api.v1.data.sample_out import SampleOut
from app.api.v1.data.sample_search_out import SampleSearchOut
from app.api.v1.search import sample_search
from app.api.v1.services import sample_service
from app.security.scope_validator import check_scope
from fastapi import APIRouter
from fastapi.param_functions import Security
from fastapi_pagination.default import Page

router = APIRouter(
    prefix='/api/v1/samples',
    tags=['samples']
)


@router.post(
    path='/',
    response_model=SampleOut,
    status_code=201,
    dependencies=[
        Security(check_scope, scopes=['urn:sample:create:v1'])
    ]
)
async def save(sample_in: SampleIn):
    return await sample_service.save(sample_in)


@router.get(
    path='/{locale}/search/',
    response_model=Page[SampleSearchOut],
    status_code=200
)
async def search_page(locale, query, page=1, size=10, sort: List[str] = None):
    return await sample_search.page(locale, query, page, size, sort)
