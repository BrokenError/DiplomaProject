from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.smartwatches.schemas import SmartwatchList, SmartwatchOut
from apps.smartwatches.services import SmartwatchService

router = APIRouter(prefix='/smartwatches', tags=['Smartwatches'])


@router.get(
    path='',
    response_model=SmartwatchList,
    name='Get smartwatches list',
    description='Get smartwatches list',
    tags=['Smartwatches']
)
async def get_list(
        smartwatch_service: SmartwatchService = Depends(SmartwatchService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        pagination: Pagination = Depends(get_pagination),
) -> SmartwatchList:
    return await smartwatch_service.list_product(
        favourite_service=favourite_service,
        pagination=pagination
    )


@router.get(
    path='/{id_smartwatch}',
    name='Get smartwatch',
    description='Get smartwatch',
    tags=['Smartwatches'],
    response_model=SmartwatchOut
)
async def get(
        id_smartwatch: int,
        smartwatch_service: SmartwatchService = Depends(SmartwatchService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected)
) -> SmartwatchOut:
    return await smartwatch_service.get_product(
        id_instance=id_smartwatch,
        favourite_service=favourite_service,
    )
