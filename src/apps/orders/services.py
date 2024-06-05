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
        self._addons_base = []

    async def check_payment(self, id_order: int, sleep_seconds: int):
        await asyncio.sleep(sleep_seconds)

        details = self.client.operation_history()
        for detail in details.operations:
            if detail.label == str(id_order) and detail.status == 'success':
                logger.info(f'Оплата заказа №{id_order}')
                order = await self.get_instance(id_instance=int(id_order))
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
        url = None
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not create empty instance.")

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        payment_method = data.get("payment_method")
        order = await self.manager.create(
            self.Model,
            data_create={
                "id_user": self.id_user,
                "payment_method": payment_method,
                "status": OrderStatus.not_paid if payment_method == self.PAYMENT_CARD else OrderStatus.assembly
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
            if product.quantity == 0:
                product.is_active = False
            if product.quantity < item.quantity:
                raise HTTPException(status_code=400, detail="Quantity must be greater than in product quantity.")
            product.quantity -= item.quantity

        if order.payment_method == self.PAYMENT_CARD:
            user = await user_service.get_instance(id_instance=self.id_user)

            payment = Quickpay(
                receiver=settings_app.YOOMONEY_RECEIVER,
                quickpay_form="shop",
                targets=f"Оплата заказа №{order.id} пользователя {user.email}",
                label=f'{order.id}',
                paymentType="SB",
                sum=data['cost'],
            )
            task = asyncio.create_task(
                self.check_payment(id_order=order.id, sleep_seconds=settings_app.PAYMENT_WAIT_SECONDS)
            )
            self.BACKGROUND_TASKS.add(task)
            task.add_done_callback(self.BACKGROUND_TASKS.discard)

            url = payment.redirected_url

        await order_item_service.manager.session.commit()
        return OrderPaymentOut(url=url)

    async def get_instance(self, id_instance: int) -> Model:
        order = (await self.manager.execute(
            self.select_visible().filter(Order.id == id_instance).options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.product)
                .selectinload(Product.photos)
            )
            .filter(Order.status != self.STATUS)
        )).scalars().first()

        for order_item in order.order_items:
            order_item.product.photos = [photo for photo in order_item.product.photos if not photo.is_banner]
        return order

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count()).select_from(query.alias())

        orders = (await self.manager.execute(
            query
            .limit(limit)
            .offset(offset)
            .options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.product)
                .selectinload(Product.photos)
            ).filter(Order.status != self.STATUS))).scalars().all()
        for order in orders:
            for order_item in order.order_items:
                order_item.product.photos = [photo for photo in order_item.product.photos if not photo.is_banner]

        return orders, (await self.manager.execute(query_count)).scalar()

    async def list(
            self,
            *,
            filters: Optional[List] = None,
            ordering: Optional[Direction] = None,
            pagination: Pagination = None,
            query: Optional[Select] = None,
            review_service: ReviewService = None
    ):
        query = select(self.Model).where(self.Model.status != self.STATUS, self.Model.id_user == self.id_user)
        result = await super().list(filters=filters, ordering=ordering, pagination=pagination, query=query)
        for order in result['items']:
            for item in order.order_items:
                if getattr(item, 'product', None) is not None:
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
        return instance
