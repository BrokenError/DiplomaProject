from fastapi import APIRouter, Depends, Query

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.products.schemas import ProductList, ProductType, SuggestionOut
from apps.products.services import ProductService
from settings import settings_app

router = APIRouter(prefix='/products', tags=['Products'])


@router.get(
    path='/type/{id_product}',
    name='Get type product',
    description=f'Get type product: {settings_app.CATEGORIES}',
    response_model=ProductType,
    tags=['Products'],
)
async def get_type_product(
        id_product: int,
        product_service: ProductService = Depends(ProductService.from_request_protected)
) -> ProductType:
    return await product_service.get_type_product(id_instance=id_product)


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


@router.get(
    path='/search',
    response_model=ProductList,
    name='Search products',
    description='Search products',
    tags=['Products']
)
async def search_list(
        query: str = Query(None, min_length=2),
        product_service: ProductService = Depends(ProductService.from_request_protected),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_protected),
        pagination: Pagination = Depends(get_pagination),
) -> ProductList:
    return await product_service.search(query, pagination=pagination, favourite_service=favourite_service)


@router.get(
    "/suggestions",
    response_model=SuggestionOut,
    name='Get product suggestions',
    description='Get product suggestions',
    tags=['Products']
)
async def get_suggestions(
        query: str = Query(None, min_length=2),
        product_service: ProductService = Depends(ProductService.from_request_protected),
) -> SuggestionOut:
    return await product_service.get_suggestions(query)
