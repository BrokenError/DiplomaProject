from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.products.queryparams import OrderingProduct
from apps.tablets.queryparams import FilterTablet
from apps.tablets.schemas import TabletList, TabletOut
from apps.tablets.services import TabletService
from dependencies import QUERYFILTER

router = APIRouter(prefix='/tablets', tags=['Tablets'])


@router.get(
    path='',
    response_model=TabletList,
    name='Get tablets list',
    description='Get tablets list',
    tags=['Tablets']
)
async def get_list(
        tablets_service: TabletService = Depends(TabletService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        model_ordering: OrderingProduct = Depends(),
        model_filter: FilterTablet = Depends(),
        pagination: Pagination = Depends(get_pagination),
) -> TabletList:
    ordering = QUERYFILTER.get_ordering(
        ordering=model_ordering)
    filters = QUERYFILTER.get_filters(
        model_db=tablets_service.Model,
        dict_filters=model_filter.dict()
    )

    return await tablets_service.list_product(
        pagination=pagination,
        ordering=ordering,
        filters=filters,
        favourite_service=favourite_service,
    )


@router.get(
    path='/{id_tablet}',
    name='Get tablet',
    description='Get tablet',
    tags=['Tablets'],
    response_model=TabletOut
)
async def get(
        id_tablet: int,
        tablet_service: TabletService = Depends(TabletService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected)
) -> TabletOut:
    return await tablet_service.get_product(
        id_instance=id_tablet,
        favourite_service=favourite_service,
    )
