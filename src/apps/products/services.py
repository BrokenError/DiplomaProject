import locale
import logging
import math
from decimal import ROUND_HALF_UP
from typing import Optional, List, Tuple, Dict, Any

from fastapi import HTTPException
from fuzzywuzzy import process
from pydantic.types import Decimal
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from apps.commons.managers.base import ManagerBase
from apps.commons.pagination.schemas import Pagination
from apps.commons.querystrings_v2.schemas import Direction
from apps.commons.services.base import ServiceBase, ServiceAuthenticate
from apps.favourites.services import FavouriteService
from apps.products.queryparams import FilterProduct, FilterSmartphone, FilterSmartwatch, FilterTelevision, FilterLaptop, \
    FilterTablet
from apps.products.schemas import ProductIn, CategoryEnum
from db.models import Product, Review, Tablet, Television, Smartphone, Smartwatch, Laptop, User
from field_names_ru import NameFilters

logger = logging.getLogger('products')


class ProductService(ServiceBase):
    Model = Product
    THRESHOLD = 50

    def __init__(self, manager: ManagerBase, id_user, *args, **kwargs) -> None:
        super().__init__(manager, id_user, *args, **kwargs)
        self.Model_filter = None
        self._addons_base = [self.Model.is_deleted.is_(False)]

    async def create(self, *, data: ProductIn = None, data_extra: Optional[dict] = None) -> Model:
        product = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(product)
        return product

    @staticmethod
    def format_price_with_spaces(number):
        return "{:,.0f}".format(number).replace(",", " ")

    def create_dynamic_price_ranges(self, min_price, max_price, num_ranges=6):
        log_min_price = math.log10(min_price)
        log_max_price = math.log10(max_price)
        log_step = (log_max_price - log_min_price) / num_ranges

        ranges = []
        for i in range(num_ranges):
            start = math.floor(10 ** (log_min_price + i * log_step))
            end = math.floor(10 ** (log_min_price + (i + 1) * log_step))
            ranges.append({
                "label": "{} - {} ₽".format(
                    self.format_price_with_spaces(start),
                    self.format_price_with_spaces(end)
                ),
                "min": start, "max": end
            })

        ranges[0]["label"] = f"Менее {self.format_price_with_spaces(ranges[0]['max'])} ₽"
        ranges[0]["min"] = None
        ranges[-1]["label"] = f"{self.format_price_with_spaces(ranges[-1]['min'])} ₽ и более"
        ranges[-1]["max"] = None

        return ranges

    async def get_filters_form(self, model: Model) -> Dict[str, Any]:
        model_data = {
            "smartphone": (FilterSmartphone(), Smartphone),
            "product": (FilterProduct(), Product),
            "smartwatch": (FilterSmartwatch(), Smartwatch),
            "television": (FilterTelevision(), Television),
            "laptop": (FilterLaptop(), Laptop),
            "tablet": (FilterTablet(), Tablet)
        }

        model = model.lower()

        if model not in model_data:
            raise HTTPException(status_code=400, detail="On this model does not exist filters")

        filter_fields = model_data[model][0].dict()

        min_max_prices = await self.manager.execute(
            select(
                func.min(Product.price).label("min_price"),
                func.max(Product.price).label("max_price")
            )
        )
        min_price, max_price = min_max_prices.fetchone()

        if min_price is None or max_price is None:
            return {}

        price_ranges = self.create_dynamic_price_ranges(min_price, max_price)
        filter_options = {}

        for field in filter_fields:
            field_key = field.split('__')[0]

            self.Model_filter = model_data[model][1]
            result = await self.manager.execute(
                select(
                    [func.json_agg(func.distinct(getattr(self.Model_filter, field_key))).label(f"{field_key}_options")]
                ).where(getattr(self.Model_filter, field_key) != None)
            )
            variants = result.scalar_one_or_none() or []
            filter_options[f"{NameFilters[field_key]}"] = {
                "id": field_key,
                "variants": variants
            }

        filter_options.update({
            f"{NameFilters['price']}": {
                "id": "price",
                "min": f"{self.format_price_with_spaces(min_price)} ₽",
                "max": f"{self.format_price_with_spaces(max_price)} ₽",
                "variants": price_ranges
            }
        })

        return filter_options

    async def search(
            self,
            query: str,
            pagination: Pagination = None,
            favourite_service: FavouriteService = None,
            filters=None,
            ordering=None,
    ):
        if not query:
            raise HTTPException(status_code=400, detail='Query is required')

        query_products = self.select_visible()

        if filters:
            for filter in filters:
                query_products = query_products.where(filter)

        if ordering is None:
            ordering = self.Model.id

        query_products = await self.choose_sort(ordering, query_products)

        products = query_products.scalars().all()

        product_data_for_search = {
            f"{CategoryEnum[product.type].value}{product.type}{product.model}{product.name}{product.material}{product.color_main}":
                product.id for product in products
        }

        matches = process.extract(query, product_data_for_search.keys())
        result_prod_ids = [
            product_data_for_search.get(f'{match[0]}', None)
            for match in matches if match[1] >= self.THRESHOLD
        ]

        products = await self.list_paginated(query=(self.get_by_ids(result_prod_ids)), pagination=pagination)
        products['items'] = sorted(products['items'], key=lambda x: result_prod_ids.index(x.id))

        for item in products['items']:
            await self.get_rating_and_reviews_count(item)
            if self.id_user:
                await self.check_product_in_cart(item)
                await self.check_favourites(item, favourite_service=favourite_service)
        return products

    async def get_suggestions(self, query: str):
        if not query:
            raise HTTPException(status_code=400, detail='Query is required')

        products_data = (
            await self.manager.execute(self.select_visible(self.Model.type, self.Model.name, self.Model.model).distinct())
        ).all()

        products_data_list = set()
        for data in products_data:
            products_data_list.update(data)
            products_data_list.add(CategoryEnum[data[0]].value)

        result_search_data = process.extract(query, list(products_data_list))
        suggestions = [data[0] for data in result_search_data if data[1] >= self.THRESHOLD]
        return dict(suggestions=suggestions)

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
        data = (await self.manager.execute(
            self.select_visible(self.Model.id, self.Model.memory)
            .where(self.Model.model == instance.model).distinct())).all()

        memory_variations = {}
        for data_product in data:
            memory_variations.update({f"{data_product.memory}": data_product.id})
        instance.memory_variations = memory_variations
        return instance

    async def get_color_variations(self, instance: Model) -> List:
        color_variations = (
            await self.manager.execute(
                select(Product.color_main, Product.color_hex, Product.id)
                .distinct()
                .where(Product.type == instance.type)
            )
        ).all()
        instance.color_variations = [
            {'color': color, 'hex': hex_value, 'id_product': id_prod} for color, hex_value, id_prod in color_variations
        ]
        return instance

    async def get_reviews(self, instance: Model) -> Model:
        reviews = (await self.manager.execute(
            select(
                Review.id, Review.rating, Review.text, Review.date_created,
                func.coalesce(
                    func.concat_ws(' ', User.first_name, User.last_name), None
                ).label('user'), User.photo_url
            )
            .outerjoin(User, Review.id_user == User.id)
            .filter(Review.id_product == instance.id)
        )).mappings().all()

        modified_reviews = []
        for review in reviews:
            review_dict = dict(review)
            modified_reviews.append(review_dict)
        instance.reviews = modified_reviews
        return instance

    async def get_product(
            self,
            id_instance: int,
            favourite_service: FavouriteService,
    ) -> Model:
        instance = (await self.manager.execute(
            self.select_visible()
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
        return instance

    async def get_instance(self, id_instance: int) -> Model:
        return (await self.manager.execute(
            self.select_visible()
            .options(selectinload(Product.photos))
            .where(self.Model.id == id_instance)
        )).scalars().first()

    async def get_type_product(self, id_instance: int) -> Model:
        product = await super().get(id_instance=id_instance)
        return product

    async def get(
            self,
            id_instance: int,
            is_auth: Optional[ServiceAuthenticate] = None,
            favourite_service: FavouriteService = None
    ) -> Model:
        product = await super().get(id_instance=id_instance)
        await self.get_rating_and_reviews_count(product)
        if self.id_user:
            await self.check_favourites(product, favourite_service)
            await self.check_product_in_cart(product)
        return product

    async def list_product(
        self,
        favourite_service: FavouriteService,
        *,
        filters: Optional[List] = None,
        ordering: Optional[Direction] = None,
        pagination: Pagination = None
    ):
        query = self.select_visible()
        result = await self.list(filters=filters, ordering=ordering, pagination=pagination, query=query)
        if self.id_user:
            for product in result['items']:
                await self.check_favourites(product, favourite_service)
                await self.check_product_in_cart(product)
        for product in result['items']:
            await self.get_rating_and_reviews_count(product)
        return result

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(
                query.limit(limit).offset(offset).options(selectinload(Product.photos)))).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )
