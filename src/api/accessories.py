from fastapi import APIRouter, Depends

from apps.accessories.schemas import AccessoryList, AccessoryOut
from apps.accessories.services import AccessoryService
from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.products.queryparams import OrderingProduct, FilterAccessory
from dependencies import QUERYFILTER

router = APIRouter(prefix='/accessories', tags=['Accessories'])


@router.get(
    path='',
    response_model=AccessoryList,
    name='Get accessories list',
    description='Get accessories list',
    tags=['Accessories']
)
async def get_list(
        accessory_service: AccessoryService = Depends(AccessoryService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        model_ordering: OrderingProduct = Depends(),
        model_filter: FilterAccessory = Depends(),
        pagination: Pagination = Depends(get_pagination),
) -> AccessoryList:
    ordering = QUERYFILTER.get_ordering(
        ordering=model_ordering)
    filters = QUERYFILTER.get_filters(
        model_db=accessory_service.Model,
        dict_filters=model_filter.dict()
    )

    return await accessory_service.list_product(
        pagination=pagination,
        ordering=ordering,
        filters=filters,
        favourite_service=favourite_service,
    )


@router.get(
    path='/{id_accessory}',
    name='Get accessory',
    description='Get accessory',
    tags=['Accessories'],
    response_model=AccessoryOut
)
async def get(
        id_accessory: int,
        accessory_service: AccessoryService = Depends(AccessoryService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected)
) -> AccessoryOut:
    return await accessory_service.get_product(
        id_instance=id_accessory,
        favourite_service=favourite_service,
    )
