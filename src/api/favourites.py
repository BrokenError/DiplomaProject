from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.schemas import FavouriteList, FavouriteIn, FavouriteOut
from apps.favourites.services import FavouriteService

router = APIRouter(prefix='/favourites', tags=['Favourites'])


@router.get(
    path='',
    name='Get favourites',
    response_model=FavouriteList,
    description='Get favourites',
    tags=['Favourites'],
)
async def favourites(
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_private),
        pagination: Pagination = Depends(get_pagination),
) -> FavouriteList:
    return await favourite_service.list_favourites(
        filters=None,
        pagination=pagination
    )


@router.post(
    path='',
    name='add favourite product',
    description='add favourite product',
    response_model=FavouriteOut,
    tags=['Favourites'],
)
async def favourites(
        data: FavouriteIn,
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_private),
) -> FavouriteOut:
    return await favourite_service.create(data=data)


@router.delete(
    path='/{id_product}',
    name='delete favourite product',
    description='delete favourite product',
    tags=['Favourites'],
)
async def favourites(
        id_product: int,
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_private),
):
    return await favourite_service.delete(id_instance=id_product)

