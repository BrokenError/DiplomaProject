import logging
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from apps.commons.basics.exceptions import ExceptionValidation
from apps.commons.services.base import ServiceBase
from apps.orders.schemas import OrderIn, OrderItemIn
from apps.products.services import ProductService
from db.models import Product, Order, \
    OrderItem, Photo

logger = logging.getLogger('orders')


class OrderService(ServiceBase):
    Model = Order

    async def create(self, *, data: OrderIn = None, data_extra: Optional[dict] = None) -> Model:
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not create empty instance.")

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()
        order = await self.manager.create(
            self.Model,
            data | {"id_user": int(self.id_user)}
        )
        await self.manager.session.refresh(order)
        return order

    async def get_instance(self, id_instance: int) -> Model:
        return (await self.manager.execute(
                self.select_visible().filter(Order.id == id_instance).options(
                    selectinload(Order.order_item)
                    .selectinload(OrderItem.product)
                    .selectinload(Product.photos).load_only(Photo.url)
                    ))
                ).scalars().first()

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(
                query.limit(limit).offset(offset).filter(Order.id_user == int(self.id_user)).options(
                    selectinload(Order.order_item)
                    .selectinload(OrderItem.product)
                    .selectinload(Product.photos).load_only(Photo.url)
                    )
            )).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )

    async def get(self, id_instance: int) -> Model:
        instance = await self.get_instance(id_instance=id_instance)
        if str(instance.id_user) == self.id_user:
            return instance
        raise HTTPException(status_code=403, detail="Доступ к этой странице ограничен")


class OrderItemService(ProductService):
    Model = OrderItem

    async def create(self, *, data: OrderItemIn = None, data_extra: Optional[dict] = None) -> Model:
        order_item = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(order_item)
        return order_item
