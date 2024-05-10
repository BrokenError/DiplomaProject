from fastapi import APIRouter, Depends

from apps.carts.schemas import CartIn, CartList, CartOut, CartUpdate
from apps.carts.services import CartService
from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService

router = APIRouter(prefix='/cart', tags=['Cart'])


@router.get(
    path='',
    name='Get products in cart',
    response_model=CartList,
    description='Get products in cart',
    tags=['Cart'],
)
async def get_list(
        cart_service: CartService = Depends(CartService.from_request_private),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_private),
        pagination: Pagination = Depends(get_pagination),
) -> CartList:
    return await cart_service.list(
        filters=None,
        pagination=pagination,
        favourite_service=favourite_service
    )


@router.post(
    path='',
    name='add product in cart',
    description='add product in cart',
    tags=['Cart'],
    response_model=CartOut,
)
async def create(
        data: CartIn,
        cart_service: CartService = Depends(CartService.from_request_private),
) -> CartOut:
    return await cart_service.add(data=data)


@router.patch(
    path='/{id_product}',
    name='add product in cart',
    description='add product in cart',
    response_model=CartOut,
    tags=['Cart']
)
async def create(
        id_product: int,
        data: CartUpdate,
        cart_service: CartService = Depends(CartService.from_request_private),
) -> CartOut:
    return await cart_service.update(data=data, id_product=id_product)


@router.delete(
    path='/{id_product}',
    name='delete product from cart',
    description='delete product from cart',
    tags=['Cart'],
)
async def delete(
        id_product: int,
        cart_service: CartService = Depends(CartService.from_request_private),
):
    return await cart_service.delete_from_cart(id_instance=id_product)

