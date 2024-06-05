import asyncio
import logging
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from yoomoney import Client, Quickpay

from apps.commons.basics.exceptions import ExceptionValidation
from apps.commons.managers.base import ManagerBase
from apps.commons.pagination.schemas import Pagination
from apps.commons.querystrings_v2.schemas import Direction
from apps.commons.services.base import ServiceBase, ServiceAuthenticate
from apps.favourites.services import FavouriteService
from apps.orders.schemas import OrderIn, OrderStatus, OrderPaymentOut
from apps.products.services import ProductService
from apps.reviews.services import ReviewService
from apps.users.services import UserService
from db.models import Product, Order, OrderItem, Photo
from settings import settings_app

logger = logging.getLogger('orders')


class OrderService(ServiceBase):
    Model = Order
    STATUS = 'cart'
    PAYMENT_CARD = 'card'
    BACKGROUND_TASKS = set()

    def __init__(self, manager: ManagerBase, id_user: [int, ServiceAuthenticate], *args, **kwargs):
        super().__init__(id_user=id_user, manager=manager, *args, **kwargs)
        self.client = Client(settings_app.TOKEN_PAYMENT)

    async def check_payment(self, id_order: int, sleep_seconds: int):
        await asyncio.sleep(sleep_seconds)
        details = self.client.operation_history()

        for detail in details.operations:
            if detail.label == str(id_order) and detail.status == 'success':
                order = await self.get_instance(id_instance=id_order)
                order.status = OrderStatus.assembly
                await self.manager.session.commit()

    async def create(
            self,
            *,
            data: OrderIn = None,
            data_extra: Optional[dict] = None,
            order_item_service=None,
            product_service: Optional[ProductService] = None,
            user_service: UserService = None,
    ) -> OrderPaymentOut:
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not create empty instance.")

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        payment_method = data.get("payment_method")
        order = await self.manager.create(
            self.Model,
            data_create={
                "id_user": self.id_user,
                "payment_method": payment_method,
                "status": OrderStatus.assembly if payment_method == 'cash' else OrderStatus.not_paid,
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
            if item is None:
                raise HTTPException(status_code=404, detail="The item does not in cart")
            item.id_order = order.id

            product = (
                await self.manager.execute(product_service.select_visible(id=item.id_product))
            ).scalars().first()
            if product.quantity < item.quantity:
                raise HTTPException(status_code=400, detail="Quantity must be greater than in product quantity.")
            product.quantity -= item.quantity
            if product.quantity == 0:
                product.is_active = False

        if order.payment_method == self.PAYMENT_CARD:
            user = self.client.account_info()

            quickpay = Quickpay(
                receiver=f"{user.account}",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=data['cost'],
                label=f"{order.id}"
            )
            task = asyncio.create_task(self.check_payment(id_order=order.id, sleep_seconds=settings_app.TIME_FOR_PAYMENT))
            self.BACKGROUND_TASKS.add(task)
            task.add_done_callback(self.BACKGROUND_TASKS.discard)

        await order_item_service.manager.session.commit()
        return OrderPaymentOut(url=quickpay.redirected_url if quickpay else None)

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
