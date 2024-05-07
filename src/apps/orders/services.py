import logging
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from apps.carts.services import CartService
from apps.commons.basics.exceptions import ExceptionValidation
from apps.commons.pagination.schemas import Pagination
from apps.commons.services.base import ServiceBase
from apps.orders.schemas import OrderIn
from db.models import Product, Order, OrderItem, Photo

logger = logging.getLogger('orders')


class OrderService(ServiceBase):
    Model = Order
    STATUS = 'cart'

    async def create(
            self,
            *,
            data: OrderIn = None,
            data_extra: Optional[dict] = None,
            order_item_service: Optional[CartService] = None) -> Model:
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not create empty instance.")

        status = {"status": data.status}

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        description = {"description": str(data['description'])}
        user = {"id_user": int(self.id_user)}

        order = await self.manager.create(
            self.Model,
            data_create=status | description | user
        )
        await self.manager.session.refresh(order)

        user_order_cart = await order_item_service.get_order_cart()

        for id_product in data['order_items']:
            item = (
                await self.manager.execute(
                    order_item_service.select_visible(
                        id_user=order.id_user,
                        id_product=id_product,
                        id_order=user_order_cart.id
                    ))
            ).scalars().first()
            if item is None:
                raise HTTPException(status_code=404, detail="The item does not in cart")
            item.id_order = order.id
            await order_item_service.manager.session.commit()

        return order

    async def get_instance(self, id_instance: int) -> Model:
        return (await self.manager.execute(
            self.select_visible().filter(Order.id == id_instance).options(
                selectinload(Order.order_item)
                .selectinload(OrderItem.product)
                .selectinload(Product.photos).load_only(Photo.url)
            )
            .filter(Order.status != 'cart')
        )).scalars().first()

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(
                query.limit(limit).offset(offset).filter(Order.id_user == self.id_user).options(
                    selectinload(Order.order_item)
                    .selectinload(OrderItem.product)
                    .selectinload(Product.photos).load_only(Photo.url)
                )
                .filter(Order.status != 'cart')
            )).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )

    async def list(
            self,
            *,
            filters: Optional[List] = None,
            orderings: Optional[List] = None,
            pagination: Pagination = None,
            query: Optional[Select] = None,
    ):
        query = select(self.Model).where(self.Model.status != self.STATUS)
        return await super().list(filters=filters, orderings=orderings, pagination=pagination, query=query)

    async def get(self, id_instance: int) -> Model:
        instance = await self.get_instance(id_instance=id_instance)
        if not instance:
            raise HTTPException(status_code=404, detail=f"The order does not exist")
        if instance.id_user != self.id_user:
            raise HTTPException(status_code=403, detail="Access denied")
        return instance
