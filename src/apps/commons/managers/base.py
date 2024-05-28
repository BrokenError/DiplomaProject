from typing import Any, Coroutine, Iterable, Type, TypeVar

from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from db.database import get_session

Base = declarative_base()

ModelType = TypeVar('ModelType', bound=Base)


class ManagerBase:

    @classmethod
    async def from_request(cls, session: AsyncSession = Depends(get_session)):
        return cls(session)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def execute(self, query) -> Coroutine:
        return self.session.execute(query)

    async def update(self, instance: ModelType, data_update: dict[str, Any]) -> ModelType:
        for field in data_update.keys():
            setattr(instance, field, data_update.get(field))

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)

        return instance

    async def create(self, model: Type[ModelType], data_create: dict[str, Any]) -> ModelType:
        instance = model(**data_create)

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)

        return instance

    async def add_all(self, instances: Iterable[ModelType]) -> Iterable[ModelType]:
        self.session.add_all(instances)
        await self.session.commit()

        return instances

    async def delete(self, instance: ModelType) -> Response:
        await self.session.delete(instance)
        await self.session.commit()

        return Response(status_code=200)

    async def delete_all(self, instances: Iterable[ModelType]) -> Response:
        for instance in instances:
            await self.session.delete(instance)
        await self.session.commit()

        return Response(status_code=200)
