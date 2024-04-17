import logging
from typing import Optional, List, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, selectin_polymorphic, joinedload
from sqlalchemy.sql import Select

from apps.commons.pagination.schemas import Pagination
from apps.commons.services.base import ServiceBase, ServiceAuthenticate
from apps.favourites.services import FavouriteService
from apps.products.schemas import ProductIn
from db.models import Product, Review, Tablet, Accessory, Television, Smartphone, Smartwatch, Laptop, User

logger = logging.getLogger('products')


class ProductService(ServiceBase):
    Model = Product

    async def create(self, *, data: ProductIn = None, data_extra: Optional[dict] = None) -> Model:
        product = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(product)
        return product

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
        return instance

    async def get_reviews(self, instance: Model) -> Model:
        instance.reviews = (await self.manager.execute(
            select(
                Review.id, Review.rating, Review.text,
                func.coalesce(
                    func.concat(User.first_name, ' ', User.last_name), None
                ).label('user')).outerjoin(User, Review.id_user == User.id)
            .filter(Review.id_product == instance.id))).all()
        return instance

    @staticmethod
    async def check_favourite(instance: Model, favourite_service) -> Model:
        instance.is_favourite = await favourite_service.check_exists(id_product=instance.id)
        return instance

    async def get_product(
            self,
            id_instance: int,
            favourite_service: FavouriteService,
    ) -> Model:
        instance = (await self.manager.execute(
            self.select_visible().options(
                selectin_polymorphic(Product, [
                    Tablet, Accessory, Television, Smartphone, Smartwatch, Laptop
                ])
            )
            .options(selectinload(Product.photos))
            .where(self.Model.id == id_instance))).scalars().first()

        instance.is_favourite = False
        await self.get_rating_and_reviews_count(instance)
        if self.id_user:
            await self.check_favourite(instance, favourite_service)
        return await self.get_reviews(instance)

    async def get_instance(self, id_instance: int) -> Model:
        return (await self.manager.execute(
            self.select_visible()
            .options(selectinload(Product.photos))
            .where(self.Model.id == id_instance)
        )).scalars().first()

    async def get(self, id_instance: int, is_auth: Optional[ServiceAuthenticate] = None) -> Model:
        product = await super().get(id_instance=id_instance)
        await self.get_rating_and_reviews_count(product)
        return product

    async def list_product(
        self,
        favourite_service: FavouriteService,
        *,
        filters: Optional[List] = None,
        orderings: Optional[List] = None,
        pagination: Pagination = None,
        query: Optional[Select] = None,
    ):
        result = await self.list(filters=filters, orderings=orderings, pagination=pagination, query=query)
        for product in result['items']:
            await self.get_rating_and_reviews_count(product)
            product.is_favourite = False

        if self.id_user:
            for product in result['items']:
                await self.check_favourite(product, favourite_service)
        return result

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(
                query.limit(limit).offset(offset).options(selectinload(Product.photos)))).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )
