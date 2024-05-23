from fastapi import Depends, APIRouter

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.laptops.schemas import LaptopList, LaptopOut
from apps.laptops.services import LaptopService
from apps.products.queryparams import OrderingProduct, FilterLaptop
from dependencies import QUERYFILTER

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
        model_ordering: OrderingProduct = Depends(),
        model_filter: FilterLaptop = Depends(),
        pagination: Pagination = Depends(get_pagination),
) -> LaptopList:
    ordering = QUERYFILTER.get_ordering(
        ordering=model_ordering)
    filters = QUERYFILTER.get_filters(
        model_db=laptop_service.Model,
        dict_filters=model_filter.dict()
    )

    return await laptop_service.list_product(
        favourite_service=favourite_service,
        ordering=ordering,
        filters=filters,
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
