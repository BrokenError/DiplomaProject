from fastapi import Depends, APIRouter

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
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
        laptop_service: LaptopService = Depends(LaptopService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        pagination: Pagination = Depends(get_pagination),
) -> LaptopList:
    return await laptop_service.list_product(
        favourite_service=favourite_service,
        pagination=pagination
    )


@router.get(
    path='/{id_laptop}',
    name='Get laptop',
    description='Get laptop',
    tags=['Laptops'],
    response_model=LaptopOut
)
async def get(
        id_laptop: int,
        laptop_service: LaptopService = Depends(LaptopService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected)
) -> LaptopOut:
    return await laptop_service.get_product(id_instance=id_laptop, favourite_service=favourite_service)
