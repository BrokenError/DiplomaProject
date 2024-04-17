import logging
from os.path import exists
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy.sql import Select, select, func

from apps.commons.pagination.schemas import Pagination
from apps.commons.services import ServiceBase
from apps.favourites.schemas import FavouriteIn
from db.models import Favourite

logger = logging.getLogger('favourites')


class FavouriteService(ServiceBase):
    Model = Favourite

    async def create(self, *, data: FavouriteIn = None, data_extra: Optional[dict] = None) -> Model:
        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        if await self.check_exists(**data):
            raise HTTPException(status_code=409, detail="Товар уже довлен в понравившиеся")
        favourite = await self.manager.create(
            self.Model,
            data | {"id_user": int(self.id_user)}
        )
        await self.manager.session.refresh(favourite)
        return favourite

    async def delete(self, id_instance: int):
        return await self.manager.delete((await self.manager.execute(
            self.select_visible().where(self.Model.id_product == id_instance))).scalars().first())

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

        if pagination is None:
            pagination = Pagination(size_page=-1, number_page=1)

        return await self.list_paginated(
            query=query,
            pagination=pagination
        )

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(
                query.limit(limit).offset(offset).filter(Favourite.id_user == int(self.id_user)))
             ).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )
