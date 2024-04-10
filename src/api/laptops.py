from fastapi import Depends, APIRouter

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.laptops.schemas import LaptopList, LaptopOut
from apps.laptops.services import LaptopService

router = APIRouter(prefix='/laptops', tags=['Laptops'])


@router.get(
    path='',
    response_model=LaptopList,
    name='Get laptops list',
    description='Get laptops list',
    tags=['Laptops']
)
async def get_list(
        laptop_service: LaptopService = Depends(LaptopService.from_request),
        pagination: Pagination = Depends(get_pagination),
) -> LaptopList:
    return await laptop_service.list(
        pagination=pagination
    )


@router.get(
    path='/{id_laptop}',
    name='Get laptop',
    description='Get laptop',
    operation_id='Get laptop',
    tags=['Laptops'],
    response_model=LaptopOut
)
async def get(
        id_laptop: int,
        laptop_service: LaptopService = Depends(LaptopService.from_request)
) -> LaptopOut:
    return await laptop_service.get(id_instance=id_laptop)
