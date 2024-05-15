from fastapi import APIRouter, Depends

from apps.carts.services import CartService
from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.favourites.services import FavouriteService
from apps.orders.schemas import OrderList, OrderOut, OrderIn, OrderCustom
from apps.orders.services import OrderService

router = APIRouter(prefix='/orders', tags=['Orders'])


@router.get(
    path='',
    response_model=OrderList,
    name='Get orders list',
    description='Get orders list',
    tags=['Orders']
)
async def get_list(
        order_service: OrderService = Depends(OrderService.from_request_private),
        pagination: Pagination = Depends(get_pagination),
) -> OrderList:
    return await order_service.list(
        filters=None,
        pagination=pagination,
    )


@router.get(
    path='/{id_order}',
    name='Get order',
    description='Get order',
    tags=['Orders'],
    response_model=OrderCustom
)
async def get(
        id_order: int,
        order_service: OrderService = Depends(OrderService.from_request_private),
        favourite_service: FavouriteService = Depends(FavouriteService.from_request_private)
) -> OrderCustom:
    return await order_service.get(id_instance=id_order, favourite_service=favourite_service)


@router.post(
    path='',
    name='Create order',
    description='Create order',
    response_model=OrderOut,
    tags=['Orders'],
)
async def create(
        data: OrderIn,
        order_service: OrderService = Depends(OrderService.from_request_private),
        order_item_service: CartService = Depends(CartService.from_request_private)
):
    return await order_service.create(data=data, order_item_service=order_item_service)
