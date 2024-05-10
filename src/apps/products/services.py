import logging
from decimal import ROUND_HALF_UP
from typing import Optional, List, Tuple

from fastapi import HTTPException
from pydantic.types import Decimal
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, selectin_polymorphic
from sqlalchemy.sql import Select

from apps.commons.managers.base import ManagerBase
from apps.commons.pagination.schemas import Pagination
from apps.commons.services.base import ServiceBase, ServiceAuthenticate
from apps.favourites.services import FavouriteService
from apps.products.schemas import ProductIn
from db.models import Product, Review, Tablet, Accessory, Television, Smartphone, Smartwatch, Laptop, User
from settings import settings_app

logger = logging.getLogger('products')


class ProductService(ServiceBase):
    Model = Product

    def __init__(self, manager: ManagerBase, id_user, *args, **kwargs) -> None:
        super().__init__(manager, id_user, *args, **kwargs)
        self._addons_base = [self.Model.is_deleted.is_(False)]

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

        if instance.average_rating is not None:
            instance.average_rating = Decimal(instance.average_rating).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
        return instance

    async def get_memory_variations(self, instance: Model) -> Model:
        instance.memory_variations = (await self.manager.execute(
            self.select_visible(self.Model.memory)
            .where(self.Model.model == instance.model).distinct())).scalars().all()
        return instance

    async def get_color_variations(self, instance: Model) -> List:
        color_variations = (
            await self.manager.execute(
                select(Product.color_main, Product.color_hex)
                .distinct()
                .where(Product.type == instance.type)
            )
        ).all()
        instance.color_variations = [{'color': color, 'hex': hex_value} for color, hex_value in color_variations]
        return instance

    async def get_reviews(self, instance: Model) -> Model:
        reviews = (await self.manager.execute(
            select(
                Review.id, Review.rating, Review.text, Review.date_created,
                func.coalesce(
                    func.concat(User.first_name, ' ', User.last_name), None
                ).label('user'), User.photo_url
            )
            .outerjoin(User, Review.id_user == User.id)
            .filter(Review.id_product == instance.id)
        )).mappings().all()

        modified_reviews = []
        for review in reviews:
            review_dict = dict(review)
            if review_dict['photo_url']:
                review_dict['photo_url'] = settings_app.BASE_URL + review_dict['photo_url']
            modified_reviews.append(review_dict)
        instance.reviews = modified_reviews
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

        if not instance:
            raise HTTPException(status_code=404, detail="Такого товара не существует")

        await self.get_rating_and_reviews_count(instance)
        await self.get_reviews(instance)
        if self.id_user:
            await self.check_favourites(instance, favourite_service)
            await self.check_product_in_cart(instance)
        if hasattr(instance, 'memory'):
            await self.get_memory_variations(instance)
        await self.get_color_variations(instance)
        self.get_updated_photo_url(instance)
        return instance

    async def get_instance(self, id_instance: int) -> Model:
        return (await self.manager.execute(
            self.select_visible()
            .options(selectinload(Product.photos))
            .where(self.Model.id == id_instance)
        )).scalars().first()

    async def get(
            self,
            id_instance: int,
            is_auth: Optional[ServiceAuthenticate] = None,
            favourite_service: FavouriteService = None
    ) -> Model:
        product = await super().get(id_instance=id_instance)
        await self.get_rating_and_reviews_count(product)
        self.get_updated_photo_url(product)
        await self.check_favourites(product, favourite_service)
        await self.check_product_in_cart(product)
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
        if self.id_user:
            for product in result['items']:
                await self.check_favourites(product, favourite_service)
                await self.check_product_in_cart(product)
        for product in result['items']:
            await self.get_rating_and_reviews_count(product)
            self.get_updated_photo_url(product)
        return result

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(
                query.limit(limit).offset(offset).options(selectinload(Product.photos)))).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )
