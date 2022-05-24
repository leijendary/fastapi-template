from typing import List, Dict, Any
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends, Security
from fastapi_pagination.default import Page
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response, StreamingResponse
from starlette.websockets import WebSocket

from app.api.v1.data.file_in import FileIn
from app.api.v1.data.sample_in import SampleIn
from app.api.v1.data.sample_list_out import SampleListOut
from app.api.v1.data.sample_out import SampleOut
from app.api.v1.data.sample_search_out import SampleSearchOut
from app.api.v1.search import sample_search
from app.api.v1.services import sample_service
from app.clients import google_client
from app.core.cache.redis_setup import cache_evict, cache_get, cache_put
from app.core.data.params import SortParams, SeekParams
from app.core.data.seek import Seek
from app.core.security import encryption
from app.core.security.scope_validator import check_scope

CACHE_KEY = "sample:v1"

router = APIRouter(
    prefix="/api/v1/samples",
    tags=["samples"]
)


@router.get(
    path="/search/",
    response_model=Page[SampleSearchOut],
    status_code=200
)
async def search_list(query, params: SortParams = Depends()):
    return await sample_search.list(query, params)


@router.get(
    path="/search/{id}/",
    response_model=SampleSearchOut,
    status_code=200
)
async def search_get(id: UUID):
    return await sample_search.get(id)


@router.post(
    path="/search/reindex/",
    response_model=Dict[str, Any],
    status_code=200
)
async def search_reindex():
    return await sample_service.reindex()


@router.get(path="/files/{bucket}/{folder}/{name}/", status_code=200)
async def file_download(bucket: str, folder: str, name: str):
    result = sample_service.file_download(bucket, folder, name)

    return StreamingResponse(
        result.body,
        headers=result.headers,
        media_type=result.media_type
    )


@router.post(path="/files/", response_model=List[str], status_code=200)
async def file_upload(body: FileIn = Depends(FileIn.as_form)):
    return sample_service.file_upload(body.bucket, body.folder, body.file)


@router.delete(path="/files/{bucket}/{folder}/{name}/", status_code=204)
async def file_delete(bucket: str, folder: str, name: str):
    sample_service.file_delete(bucket, folder, name)


@router.post(path="/encrypt/", status_code=200)
async def encrypt(plaintext: str):
    return encryption.encrypt(plaintext)


@router.post(path="/decrypt/", status_code=200)
async def decrypt(encrypted: str):
    return encryption.decrypt(encrypted)


@router.get(path="/client/", status_code=200)
async def client():
    response = await google_client.home_page()

    return HTMLResponse(response)


@router.websocket("/{id}", "sample.listen")
async def listen(
        websocket: WebSocket,
        id: UUID,
        _=Security(check_scope, scopes=["urn:sample:listen:v1"])
):
    await sample_service.listen(websocket, CACHE_KEY, id)


@router.get(
    path="/",
    response_model=Seek[SampleListOut],
    status_code=200,
    dependencies=[Security(check_scope, scopes=["urn:sample:list:v1"])]
)
async def seek(query="", params: SeekParams = Depends()):
    return await sample_service.seek(query, params)


@router.get(
    path="/{id}/",
    response_model=SampleOut,
    status_code=200,
    dependencies=[Security(check_scope, scopes=["urn:sample:get:v1"])]
)
@cache_get(namespace=CACHE_KEY)
# Request and response are here to cater the headers for caching
async def get(id: UUID, request: Request, response: Response):
    return await sample_service.get(id)


@router.post(
    path="/",
    response_model=SampleOut,
    status_code=201,
    dependencies=[Security(check_scope, scopes=["urn:sample:create:v1"])]
)
@cache_put(namespace=CACHE_KEY)
# Request is here to cater the headers for caching
async def save(sample_in: SampleIn, request: Request):
    return await sample_service.save(sample_in)


@router.put(
    path="/{id}/",
    response_model=SampleOut,
    status_code=200,
    dependencies=[Security(check_scope, scopes=["urn:sample:update:v1"])]
)
@cache_put(namespace=CACHE_KEY, publish=True)
# Request is here to cater the headers for caching
async def update(id: UUID, sample_in: SampleIn, request: Request):
    return await sample_service.update(id, sample_in)


@router.delete(
    path="/{id}/",
    status_code=204,
    dependencies=[Security(check_scope, scopes=["urn:sample:delete:v1"])]
)
@cache_evict(namespace=CACHE_KEY)
async def delete(id: UUID):
    await sample_service.delete(id)
