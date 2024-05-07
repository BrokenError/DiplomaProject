import logging
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select, select, func

from apps.commons.pagination.schemas import Pagination
from apps.commons.services import ServiceBase
from apps.favourites.schemas import FavouriteIn
from db.models import Favourite, Product, Review

logger = logging.getLogger('favourites')


class FavouriteService(ServiceBase):
    Model = Favourite

    async def create(self, *, data: FavouriteIn = None, data_extra: Optional[dict] = None) -> Model:
        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        await self.check_product_or_404(data)

        if await self.check_exists(**data):
            raise HTTPException(status_code=409, detail="The product already added in favourites")
        favourite = await self.manager.create(
            self.Model,
            data | {"id_user": int(self.id_user)}
        )
        await self.manager.session.refresh(favourite)
        return favourite

    async def delete(self, id_instance: int):
        instance = (await self.manager.execute(
            self.select_visible().where(
                self.Model.id_product == id_instance,
                self.Model.id_user == int(self.id_user))
        )).scalars().first()
        if not instance:
            raise HTTPException(status_code=404, detail="The product not in favourites")

        return await self.manager.delete(instance)

    async def list(
        self,
        *,
        filters: Optional[List] = None,
        orderings: Optional[List] = None,
        pagination: Pagination = None,
        query: Optional[Select] = None,
    ):
        if query is None:
            query = self.select_visible(id_user=self.id_user)

        if filters:
            for filter in filters:
                query = query.where(filter)

        if pagination is None:
            pagination = Pagination(size_page=-1, number_page=1)

        return await self.list_paginated(
            query=query,
            pagination=pagination
        )

    async def list_favourites(
            self,
            *,
            filters: Optional[List] = None,
            orderings: Optional[List] = None,
            pagination: Pagination = None,
            query: Optional[Select] = None,
    ):
        result = await self.list(filters=filters, orderings=orderings, pagination=pagination, query=query)
        for product in result['items']:
            await self.get_rating_and_reviews_count(product.product)
            product.product.is_favourite = True
        return result

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(
                query.options(
                    selectinload(Favourite.product).selectinload(Product.photos)
                )
                .join(Favourite.product)
                .filter(Favourite.id_user == int(self.id_user))
                .offset(offset)
            )).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )

    async def get_rating_and_reviews_count(self, instance: Model) -> Model:
        reviews_count_subquery = (
            select(func.count(Review.id))
            .where(Review.id_product == instance.id)
            .scalar_subquery()
        )
        average_rating_subquery = (
            select(func.avg(Review.rating))
            .where(Review.id_product == instance.id)
            .scalar_subquery()
        )

        instance.reviews_count, instance.average_rating = (
            await self.manager.execute(
                select([reviews_count_subquery, average_rating_subquery])
            )
        ).first()

        if instance.average_rating is not None:
            instance.average_rating = Decimal(instance.average_rating).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
        return instance
