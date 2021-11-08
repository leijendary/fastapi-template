from app.data.data_response import DataResponse
from app.v1.data.sample_in import SampleIn
from app.v1.data.sample_out import SampleOut
from app.v1.services import sample_service
from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1/samples',
    tags=['samples']
)


@router.get(path='/')
async def page():
    return {}


@router.post(
    path='/',
    response_model=DataResponse[SampleOut],
    status_code=201
)
async def save(sample_in: SampleIn):
    response = await sample_service.save(sample_in)

    return DataResponse(response, 201)
