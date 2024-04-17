from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.products.schemas import ProductList, ProductType
from apps.products.services import ProductService

router = APIRouter(prefix='/products', tags=['Products'])


@router.get(
    path='/{id_product}',
    name='Get product',
    description='Get product',
    tags=['Products'],
)
async def get(
        id_product: int,
        product_service: ProductService = Depends(ProductService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
):
    return await product_service.get_product(
        id_instance=id_product,
        favourite_service=favourite_service
    )


@router.get(
    path='/type/{id_product}',
    name='Get type product',
    description='Get type product',
    response_model=ProductType,
    tags=['Products'],
)
async def get_type_product(
        id_product: int,
        product_service: ProductService = Depends(ProductService.from_request),
) -> ProductType:
    return await product_service.get(id_instance=id_product)


@router.get(
    path='',
    response_model=ProductList,
    name='Get products list',
    description='Get products list',
    tags=['Products']
)
async def get_list(
        product_service: ProductService = Depends(ProductService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        pagination: Pagination = Depends(get_pagination),
) -> ProductList:
    return await product_service.list_product(
        favourite_service=favourite_service,
        filters=None,
        pagination=pagination,
    )
