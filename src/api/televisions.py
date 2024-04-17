from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.commons.services.base import ServiceAuthenticate
from apps.favourites.services import FavouriteService
from apps.televisions.schemas import TelevisionList, TelevisionOut
from apps.televisions.services import TelevisionService

router = APIRouter(prefix='/televisions', tags=['Televisions'])


@router.get(
    path='',
    response_model=TelevisionList,
    name='Get televisions list',
    description='Get televisions list',
    tags=['Televisions']
)
async def get_list(
        smartwatch_service: TelevisionService = Depends(TelevisionService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        pagination: Pagination = Depends(get_pagination),
) -> TelevisionList:
    return await smartwatch_service.list_product(
        pagination=pagination,
        favourite_service=favourite_service,
    )


@router.get(
    path='/{id_television}',
    response_model=TelevisionOut,
    name='Get television',
    description='Get television',
    tags=['Televisions']
)
async def get_list(
        id_television: int,
        smartwatch_service: TelevisionService = Depends(TelevisionService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected)
) -> TelevisionOut:
    return await smartwatch_service.get_product(
        id_instance=id_television,
        favourite_service=favourite_service,
    )
