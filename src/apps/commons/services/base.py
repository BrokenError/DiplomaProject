from datetime import datetime, timedelta
from typing import Optional, Iterable, List, Any, Generator

from fastapi import Depends, HTTPException, Request
from jose import jwt
from jose.exceptions import JWTError
from pydantic import BaseModel
from sqlalchemy import exists, inspect, select, Column, func, desc, and_, asc, nullslast, case, cast, Float
from sqlalchemy.sql import Executable, Select

from apps.commons.basics.exceptions import ExceptionValidation
from apps.commons.managers.base import ManagerBase
from apps.commons.pagination.mixins import MixinPagination
from apps.commons.pagination.schemas import Pagination
from apps.commons.querystrings_v2.schemas import Direction
from apps.commons.services.interface import InterfaceService
from apps.orders.schemas import OrderStatus
from db.models import Product, Order, OrderItem, Review
from settings import settings_app


class ServiceAuthenticate:

    @staticmethod
    def private(request: Request):
        try:
            token = request.headers["Authorization"].split("Bearer ")[-1]
            token_decoded = jwt.decode(token, settings_app.SECRET_KEY, algorithms=[settings_app.ALGORITHM])
            return token_decoded["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except (jwt.JWTError, KeyError, ValueError):
            raise HTTPException(status_code=400, detail="Token invalid")

    @staticmethod
    def protected(request: Request):
        try:
            token = request.headers["Authorization"].split("Bearer ")[-1]
            token_decoded = jwt.decode(token, settings_app.SECRET_KEY, algorithms=[settings_app.ALGORITHM])
            return token_decoded["sub"]
        except (JWTError, KeyError, ValueError):
            return False


class ServiceBase(InterfaceService, MixinPagination):
    Model = None

    def __init__(self, manager: ManagerBase, id_user: [int, ServiceAuthenticate], *args, **kwargs) -> None:
        self.manager = manager
        self.id_user: Optional[int, ServiceAuthenticate] = int(id_user)
        self._addons_base: Optional[Any] = []

        super().__init__(*args, **kwargs)

    def __init_subclass__(cls, **kwargs):
        assert cls.Model, 'Model for ServiceBase is not set'

        super().__init_subclass__()

    async def execute(self, query: Executable):
        return await self.manager.execute(query)

    @classmethod
    def from_request(
            cls,
            id_user: [int, ServiceAuthenticate],
            manager: ManagerBase = Depends(ManagerBase.from_request)
    ):

        return cls(manager=manager, id_user=id_user)

    @classmethod
    def from_request_private(
            cls,
            id_user: [int, ServiceAuthenticate] = Depends(ServiceAuthenticate.private),
            manager: ManagerBase = Depends(ManagerBase.from_request)
    ):
        return cls(manager=manager, id_user=id_user)

    @classmethod
    def from_request_protected(
            cls,
            id_user: [int, ServiceAuthenticate] = Depends(ServiceAuthenticate.protected),
            manager: ManagerBase = Depends(ManagerBase.from_request)
    ):
        return cls(manager=manager, id_user=id_user)

    async def check_product_in_cart(self, instance: Model) -> Model:
        is_in_cart = (await self.manager.execute(
            select(exists()
                   .where(Order.id_user == self.id_user)
                   .where(Order.id == OrderItem.id_order)
                   .where(Order.status == OrderStatus.cart)
                   .where(OrderItem.id_user == self.id_user)
                   .where(OrderItem.id_product == instance.id))
        )).scalar()
        if is_in_cart:
            instance.is_in_cart = is_in_cart
        return instance

    async def check_favourites(self, instance: Model, favourite_service) -> Model:
        instance.is_favourite = await favourite_service.check_exists(id_product=instance.id, id_user=self.id_user)
        return instance

    async def validate_data(self, id_instance: Optional[int], data: BaseModel) -> BaseModel:
        return data

    async def validate_instance(self, instance: Model) -> Model:
        raise NotImplemented("This method is deprecated. Remove it's uses.")

    def convert_to_conditions(self, conditions: dict[str, Any]) -> Generator[Column, None, None]:
        for attr, value in conditions.items():
            yield getattr(self.Model, attr) == value

    def _get_conditions(self, conditions: dict[str, Any]):
        yield from self._addons_base
        yield from self.convert_to_conditions(conditions)

    def select_visible(self, *fields, **conditions) -> Select:
        selects = fields if fields else (self.Model,)
        query = select(*selects)
        for condition in self._get_conditions(conditions):
            query = query.where(condition)

        return query

    async def create(self, *, data: Optional[BaseModel] = None, data_extra: Optional[dict] = None) -> Model:
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not create empty instance.")

        if data_extra is None:
            data_extra = dict()

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()
        instance = await self.manager.create(
            self.Model,
            data | {'id_author': self.id_user, 'id_editor_last': self.id_user} | data_extra
        )
        return instance

    async def get_instance(self, id_instance: int) -> Model:
        return (await self.manager.execute(
            self.select_visible().where(self.Model.id == id_instance)
        )).scalars().first()

    async def get(self, id_instance: int) -> Model:
        instance = await self.get_instance(id_instance)
        if not instance:
            raise HTTPException(status_code=404, detail="Такого объекта не существует")
        return instance

    async def list(
        self,
        *,
        filters: Optional[List] = None,
        ordering: Optional[Direction] = None,
        pagination: Pagination = None,
        query: Optional[Select] = None,
    ):

        if query is None:
            query = self.select_visible()

        if filters:
            for filter in filters:
                query = query.where(filter)

        if ordering is None:
            ordering = desc(self.Model.id)

        query = self.choose_sort(ordering, query)

        if pagination is None:
            pagination = Pagination(size_page=-1, number_page=1)

        return await self.list_paginated(
            query=query,
            pagination=pagination,
        )

    def choose_sort(self, ordering: Direction, query: Select) -> Select:
        match ordering:
            case Direction.popular.value:
                start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                end_of_month = start_of_month + timedelta(days=30)

                order_ids_subquery = (
                    select(Order.id)
                    .where(and_(Order.date_created >= start_of_month, Order.date_created <= end_of_month))
                    .alias("order_ids_subquery")
                )

                sales_count_subquery = (
                    select(
                        OrderItem.id_product,
                        func.count().label('sales_count')
                    )
                    .where(OrderItem.id_order.in_(select(order_ids_subquery)))
                    .group_by(OrderItem.id_product)
                    .alias("sales_count_subquery")
                )

                query = (
                    query.outerjoin(
                        sales_count_subquery, Product.id == sales_count_subquery.c.id_product
                    )
                    .order_by(nullslast(desc(sales_count_subquery.c.sales_count)))
                )
            case Direction.price_desc | Direction.price_asc:
                final_price = case(
                    [
                        (Product.discount > 0, Product.price * (1 - cast(Product.discount, Float) / 100))
                    ],
                    else_=Product.price
                ).label('final_price')

                query = query.add_columns(final_price)

                if ordering == Direction.price_desc:
                    query = query.order_by(desc('final_price'))
                else:
                    query = query.order_by(asc('final_price'))
            case Direction.discount_desc:
                query = query.order_by(desc(Product.discount))
            case Direction.rating_desc:
                query = query.add_columns(
                    func.count(Review.id).label("reviews_count"),
                    func.avg(Review.rating).label("average_rating")
                ).outerjoin(
                    Review, Review.id_product == Product.id
                ).group_by(
                    Product.id, *self.Model.__table__.columns
                ).order_by(nullslast(desc('average_rating')))
            case _:
                query = query.order_by(ordering)
        return query

    async def update(
        self,
        id_instance: Optional[int] = None,
        *,
        data: Optional[BaseModel] = None,
        data_extra: Optional[dict] = None
    ) -> Model:
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not update to empty instance.")

        if data_extra is None:
            data_extra = dict()

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        return await self.manager.update(
            await self.get(id_instance),
            data | {'id_editor_last': self.id_user} | data_extra
        )

    async def delete(self, id_instance: int) -> Model:
        return await self.manager.update(
            await self.get(id_instance),
            {
                'is_deleted': True,
                'id_editor_last': self.id_user
            }
        )

    async def delete_completely(self):
        """Delete all instances that marked is_deleted"""
        query = select(self.Model).where(self.Model.is_deleted.is_(True))
        instances = (await self.manager.execute(query)).scalars().all()
        for instance in instances:
            await self.manager.delete(instance=instance)

    async def copy(self, id_instance: int):
        instance = await self.get(id_instance)
        dict_instance = {column.key: getattr(instance, column.key) for column in inspect(instance).mapper.column_attrs}
        return await self.manager.create(
            self.Model,
            dict_instance | {'id_author': self.id_user, 'id_editor_last': self.id_user}
        )

    def get_by_ids(self, ids_instances: Iterable) -> Select:
        return select(self.Model).where(self.Model.id.in_(set(ids_instances)))

    async def get_instances_by_ids(self, ids_instances: Iterable) -> List[Model]:
        return (await self.manager.execute(
            query=self.select_visible().where(self.Model.id.in_(set(ids_instances)))
        )).scalars().all()

    async def check_exists(self, **conditions):
        return (await self.manager.execute(
            query=exists(self.select_visible(**conditions)).select()
        )).scalar()

    async def check_product_or_404(self, data):
        if not (await self.manager.execute(
            exists(select(Product).where(Product.id == data['id_product'])).select()
        )).scalar():
            raise HTTPException(404,  detail='Product not found')
        return True
