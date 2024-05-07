from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql import Select

from apps.carts.schemas import CartIn, CartUpdate
from apps.commons.pagination.schemas import Pagination
from apps.commons.services import ServiceBase
from db.models import OrderItem, Order, Product


class CartService(ServiceBase):
    Model = OrderItem
    STATUS = 'cart'

    async def add(
            self, *,
            data: Optional[CartIn] = None,
    ) -> Model:
        user_order_cart = await self.get_order_cart()

        await self.check_product_or_404(data)

        if await self.check_exists(
                id_user=self.id_user,
                id_order=user_order_cart.id,
                id_product=data.id_product
        ):
            raise HTTPException(409, detail='Product already added. Use patch to update quantity')
        return (await self.manager.create(
            model=self.Model,
            data_create=dict(data) | {"id_user": int(self.id_user), "id_order": user_order_cart.id},
        ))

    async def list(
        self,
        *,
        filters: Optional[List] = None,
        orderings: Optional[List] = None,
        pagination: Pagination = None,
        query: Optional[Select] = None,
    ):
        user_order_cart = await self.get_order_cart()

        if query is None:
            query = self.select_visible(id_user=self.id_user, id_order=user_order_cart.id)

        if filters:
            for filter in filters:
                query = query.where(filter)

        if orderings is None:
            orderings = self.Model.id,

        for ordering in orderings:
            query = query.order_by(ordering)

        if pagination is None:
            pagination = Pagination(size_page=-1, number_page=1)

        return await self.list_paginated(
            query=query,
            pagination=pagination
        )

    async def get_order_cart(self):
        return (await self.manager.execute(
            select(Order)
            .options(joinedload(Order.order_item))
            .where(Order.status == self.STATUS)
            .where(Order.id_user == int(self.id_user))
        )).scalars().first()

    async def update(
            self,
            id_product: Optional[int] = None,
            *,
            data: Optional[CartUpdate] = None,
            data_extra: Optional[dict] = None
    ) -> Model:
        order = await self.get_order_cart()

        if not await self.check_exists(id_user=self.id_user, id_order=order.id, id_product=id_product):
            raise HTTPException(status_code=404, detail="Product not found in cart")

        updated_order_item = await self.manager.update(
            instance=(await self.manager.execute(self.select_visible(
                id_user=self.id_user,
                id_order=order.id,
                id_product=id_product)
            )).scalars().first(),
            data_update={"quantity": self.Model.quantity + data.quantity}
        )
        return updated_order_item

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (
                await self.manager.execute(
                    query.limit(limit)
                    .options(selectinload(OrderItem.product).selectinload(Product.photos))
                    .join(OrderItem.product)
                    .filter(OrderItem.id_user == int(self.id_user))
                    .offset(offset)
                    .join(Order)
                    .where(Order.status == self.STATUS)
                    .where(self.Model.id_order == Order.id)
                )
            ).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )

    async def delete_from_cart(self, id_instance: int):
        user_order_cart = await self.get_order_cart()
        instance = (await self.manager.execute(
            self.select_visible().where(
                self.Model.id_product == id_instance,
                self.Model.id_user == int(self.id_user),
                self.Model.id_order == user_order_cart.id
            )
        )).scalars().first()
        if not instance:
            raise HTTPException(status_code=404, detail="Product not found in cart")
        return await self.manager.delete(instance)





