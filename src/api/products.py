from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.products.schemas import ProductList
from apps.products.services import ProductService

router = APIRouter(prefix='/products', tags=['Products'])


@router.get(
    path='/{id_product}',
    name='Get product',
    description='Get product',
    operation_id='Get product',
    tags=['Products'],
)
async def get(
        id_product: int,
        product_service: ProductService = Depends(ProductService.from_request)
):
    return await product_service.get_product(id_instance=id_product)


@router.get(
    path='',
    response_model=ProductList,
    name='Get new products list',
    description='Get new products list',
    tags=['Products']
)
async def get_list(
        product_service: ProductService = Depends(ProductService.from_request),
        pagination: Pagination = Depends(get_pagination),
) -> ProductList:
    return await product_service.list(
        filters=None,
        pagination=pagination
    )
