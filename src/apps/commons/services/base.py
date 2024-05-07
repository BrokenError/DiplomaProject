from typing import Optional, Iterable, List, Any, Generator

from fastapi import Depends, HTTPException, Request
from jose import jwt
from jose.exceptions import JWTError
from pydantic import BaseModel
from sqlalchemy import exists, inspect, select, Column
from sqlalchemy.sql import Executable, Select

from apps.commons.basics.exceptions import ExceptionValidation
from apps.commons.managers.base import ManagerBase
from apps.commons.pagination.mixins import MixinPagination
from apps.commons.pagination.schemas import Pagination
from apps.commons.services.interface import InterfaceService
from db.models import Product
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
            jwt.decode(token, settings_app.SECRET_KEY, algorithms=[settings_app.ALGORITHM])
            return True
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
            raise HTTPException(status_code=404, detail="Такого товара не существует")
        return instance

    async def list(
        self,
        *,
        filters: Optional[List] = None,
        orderings: Optional[List] = None,
        pagination: Pagination = None,
        query: Optional[Select] = None,
    ):

        if query is None:
            query = self.select_visible()

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
            exists(select(Product).where(Product.id == data.id_product)).select()
        )).scalar():
            raise HTTPException(404,  detail='Product not found')
        return True
