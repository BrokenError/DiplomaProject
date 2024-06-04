from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.products.queryparams import OrderingProduct
from apps.televisions.queryparams import FilterTelevision
from apps.televisions.schemas import TelevisionList, TelevisionOut
from apps.televisions.services import TelevisionService
from dependencies import QUERYFILTER

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
        model_ordering: OrderingProduct = Depends(),
        model_filter: FilterTelevision = Depends(),
        pagination: Pagination = Depends(get_pagination),
) -> TelevisionList:
    ordering = QUERYFILTER.get_ordering(
        ordering=model_ordering)
    filters = QUERYFILTER.get_filters(
        model_db=smartwatch_service.Model,
        dict_filters=model_filter.dict()
    )

    return await smartwatch_service.list_product(
        pagination=pagination,
        ordering=ordering,
        filters=filters,
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
