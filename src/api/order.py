from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.orders.schemas import OrderList, OrderOut, OrderIn
from apps.orders.services import OrderService
from apps.smartphones.schemas import SmartphoneOut

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
    response_model=OrderOut
)
async def get(
        id_order: int,
        order_service: OrderService = Depends(OrderService.from_request_private),
) -> OrderOut:
    return await order_service.get(id_instance=id_order)


@router.post(
    path='',
    name='Create order',
    description='Create order',
    response_model=OrderIn,
    tags=['Orders'],
)
async def create(
        data: OrderIn,
        order_service: OrderService = Depends(OrderService.from_request_private),
) -> SmartphoneOut:
    return await order_service.create(data=data)

