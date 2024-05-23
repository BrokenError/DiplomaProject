from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.products.queryparams import FilterSmartphone, OrderingProduct
from apps.smartphones.schemas import SmartphoneList, SmartphoneOut
from apps.smartphones.services import SmartphoneService
from dependencies import QUERYFILTER

router = APIRouter(prefix='/smartphones', tags=['Smartphones'])


@router.get(
    path='',
    response_model=SmartphoneList,
    name='Get smartphones list',
    description='Get smartphones list',
    tags=['Smartphones']
)
async def get_list(
        smartphone_service: SmartphoneService = Depends(SmartphoneService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        model_ordering: OrderingProduct = Depends(),
        model_filter: FilterSmartphone = Depends(),
        pagination: Pagination = Depends(get_pagination),
) -> SmartphoneList:
    ordering = QUERYFILTER.get_ordering(
        ordering=model_ordering)
    filters = QUERYFILTER.get_filters(
        model_db=smartphone_service.Model,
        dict_filters=model_filter.dict()
    )

    return await smartphone_service.list_product(
        favourite_service=favourite_service,
        ordering=ordering,
        filters=filters,
        pagination=pagination,
    )


@router.get(
    path='/{id_smartphone}',
    name='Get smartphone',
    description='Get smartphone',
    tags=['Smartphones'],
    response_model=SmartphoneOut
)
async def get(
        id_smartphone: int,
        smartphone_service: SmartphoneService = Depends(SmartphoneService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected)
) -> SmartphoneOut:
    return await smartphone_service.get_product(
        id_instance=id_smartphone,
        favourite_service=favourite_service,
    )
