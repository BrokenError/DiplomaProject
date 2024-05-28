import logging
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from apps.carts.services import CartService
from apps.commons.basics.exceptions import ExceptionValidation
from apps.commons.pagination.schemas import Pagination
from apps.commons.querystrings_v2.schemas import Direction
from apps.commons.services.base import ServiceBase
from apps.favourites.services import FavouriteService
from apps.orders.schemas import OrderIn, OrderStatus
from apps.products.services import ProductService
from apps.reviews.services import ReviewService
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
            order_item_service: Optional[CartService] = None,
            product_service: Optional[ProductService] = None
    ) -> Model:
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not create empty instance.")

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        order = await self.manager.create(
            self.Model,
            data_create={
                "id_user": self.id_user,
                "payment_method": data.get("payment_method"),
                "status": OrderStatus.ASSEMBLY,
            }
        )

        user_order_cart = await order_item_service.get_order_cart()

        for id_order_item in data['ids_order_items']:
            item = (
                await self.manager.execute(
                    order_item_service.select_visible(
                        id_user=order.id_user,
                        id=id_order_item,
                        id_order=user_order_cart.id
                    ))
            ).scalars().first()
            product = (
                await self.manager.execute(product_service.select_visible(id=item.id_product))
            ).scalars().first()
            if product.quantity < item.quantity:
                raise HTTPException(status_code=400, detail="Quantity must be greater than in product quantity.")
            product.quantity -= item.quantity
            if item is None:
                raise HTTPException(status_code=404, detail="The item does not in cart")
            item.id_order = order.id
        await order_item_service.manager.session.commit()

        return order

    async def get_instance(self, id_instance: int) -> Model:
        return (await self.manager.execute(
            self.select_visible().filter(Order.id == id_instance).options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.product)
                .selectinload(Product.photos).load_only(Photo.url)
            )
            .filter(Order.status != self.STATUS)
        )).scalars().first()

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count()).select_from(query.alias())

        return ((await self.manager.execute(
            query
            .limit(limit)
            .offset(offset)
            .options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.product)
                .selectinload(Product.photos).load_only(Photo.url)
            ).filter(Order.status != self.STATUS))).scalars().all(),
            (await self.manager.execute(query_count)).scalar())

    async def list(
            self,
            *,
            filters: Optional[List] = None,
            ordering: Optional[Direction] = None,
            pagination: Pagination = None,
            query: Optional[Select] = None,
            review_service: ReviewService = None
    ):
        query = select(self.Model).where(self.Model.status != self.STATUS)
        result = await super().list(filters=filters, ordering=ordering, pagination=pagination, query=query)
        for order in result['items']:
            for item in order.order_items:
                item.product.id_review = await review_service.get_instance_by_id_product(
                    id_product=item.product.id
                )
        return result

    async def get(
            self,
            id_instance: int,
            favourite_service: FavouriteService = None,
            review_service: ReviewService = None
    ) -> Model:
        instance = await self.get_instance(id_instance=id_instance)
        if not instance:
            raise HTTPException(status_code=404, detail=f"The order does not exist")
        if instance.id_user != self.id_user:
            raise HTTPException(status_code=403, detail="Access denied")
        for order_item in instance.order_items:
            order_item.product.id_review = await review_service.get_instance_by_id_product(
                id_product=order_item.product.id
            )
            await self.check_product_in_cart(order_item.product)
            await self.check_favourites(order_item.product, favourite_service)
        return instance
