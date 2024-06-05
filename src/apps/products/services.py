import logging
import math
from decimal import ROUND_HALF_UP
from typing import Optional, List, Tuple, Dict, Any

from fastapi import HTTPException
from fuzzywuzzy import process
from pydantic.types import Decimal
from sqlalchemy import func, select, extract, Float
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy.sql import Select, cast, case

from apps.accessories.queryparams import FilterAccessory
from apps.commons.managers.base import ManagerBase
from apps.commons.pagination.schemas import Pagination
from apps.commons.querystrings_v2.schemas import Direction
from apps.commons.services.base import ServiceBase, ServiceAuthenticate
from apps.favourites.services import FavouriteService
from apps.laptops.queryparams import FilterLaptop
from apps.products.queryparams import FilterProduct
from apps.products.schemas import ProductAdminSchema, CategoryEnum
from apps.smartphones.queryparams import FilterSmartphone
from apps.smartwatches.queryparams import FilterSmartwatch
from apps.tablets.queryparams import FilterTablet
from apps.televisions.queryparams import FilterTelevision
from db.models import Product, Review, Tablet, Television, Smartphone, Smartwatch, Laptop, User, Accessory, Photo, \
    product_photo
from field_names_ru import NameFilters

logger = logging.getLogger('products')


class ProductService(ServiceBase):
    Model = Product
    THRESHOLD = 50
    FILTER_KEY_DELETED = ('price__lte', 'price__gte')

    def __init__(self, manager: ManagerBase, id_user, *args, **kwargs) -> None:
        super().__init__(manager, id_user, *args, **kwargs)
        self.Model_filter = None
        self._addons_base = [self.Model.is_deleted.is_(False)]

    async def create(self, *, data: ProductAdminSchema = None, data_extra: Optional[dict] = None) -> Model:
        product = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(product)
        return product

    async def get_photos_slider(self):
        banner_photos_query = (
            select(
                Photo.url.label('link'),
                func.max(Product.id).label('id_product')
            )
            .select_from(Photo)
            .join(product_photo, Photo.id == product_photo.c.id_photo)
            .join(Product, product_photo.c.id_product == Product.id)
            .where(Photo.is_banner == True)
            .where(Product.is_deleted == False)
            .group_by(Photo.id)
        )
        banner_photos_result = await self.manager.session.execute(banner_photos_query)
        banner_photos_data = banner_photos_result.fetchall()

        return banner_photos_data

    @staticmethod
    def format_price_with_spaces(number):
        return "{:,.0f}".format(number).replace(",", " ")

    @staticmethod
    def best_price(price):
        magnitude = 10 ** (len(str(price)) - 1)
        return (price // magnitude) * magnitude

    def create_dynamic_price_ranges(self, min_price, max_price, num_ranges=6):
        log_min_price = math.log10(min_price)
        log_max_price = math.log10(max_price)
        log_step = (log_max_price - log_min_price) / num_ranges

        ranges = []
        for i in range(num_ranges):
            start = math.floor(10 ** (log_min_price + i * log_step))
            end = math.floor(10 ** (log_min_price + (i + 1) * log_step))
            start, end = self.best_price(start) + 1, self.best_price(end)
            ranges.append({
                "label": "{} - {} ₽".format(self.format_price_with_spaces(start),
                                            self.format_price_with_spaces(end)),
                "min": start,
                "max": end
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
            "tablet": (FilterTablet(), Tablet),
            "accessory": (FilterAccessory(), Accessory)
        }

        if not model or model.lower() not in model_data:
            raise HTTPException(status_code=400, detail="On this model does not exist filters")

        model = model.lower()
        self.Model_filter = model_data[model][1]

        min_max_prices = await self.manager.execute(
            select(
                func.count().label('count_prices'),
                func.min(
                    case(
                        [(self.Model_filter.discount > 0,
                          self.Model_filter.price * (1 - cast(self.Model_filter.discount, Float) / 100))],
                        else_=self.Model_filter.price
                    )
                ).label("min_price"),
                func.max(
                    case(
                        [(self.Model_filter.discount > 0,
                          self.Model_filter.price * (1 - cast(self.Model_filter.discount, Float) / 100))],
                        else_=self.Model_filter.price
                    )
                ).label("max_price")
            ).where(self.Model_filter.is_deleted == False)
        )
        count_prices, min_price, max_price = min_max_prices.fetchone()

        if min_price is None or max_price is None:
            return {}
        price_ranges = self.create_dynamic_price_ranges(min_price, max_price, num_ranges=2 if count_prices < 6 else 6)

        filter_fields = model_data[model][0].dict()
        filters = []

        for key in self.FILTER_KEY_DELETED:
            filter_fields.pop(key, None)

        for field in filter_fields:
            field_key = field.split('__')[0]

            query = select(
                func.json_agg(func.distinct(getattr(self.Model_filter, field_key))).label(f"{field_key}_options"))

            if field_key == 'date_release':
                query = select(
                    func.json_agg(func.distinct(extract('year', getattr(self.Model_filter, field_key)))).label(
                        f"{field_key}_options"))

            result = await self.manager.execute(
                query.where(
                    getattr(self.Model_filter, field_key) is not None,
                    self.Model_filter.is_deleted == False
                )
            )
            variants = result.scalar_one_or_none() or []
            filters.append({
                "id": field_key,
                "label": NameFilters[field_key],
                "variants": variants
            })

        filter_options = {"product_filters": filters}
        filter_options.update({
            f"price": {
                "id": "price",
                "label": NameFilters['price'],
                "min": int(min_price),
                "max": int(max_price),
                "label_min": f"{self.format_price_with_spaces(min_price)} ₽",
                "label_max": f"{self.format_price_with_spaces(max_price)} ₽",
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

        query_products = self.choose_sort(ordering, query_products)

        products = (await self.manager.execute(query_products)).scalars().all()

        product_data_for_search = {
            f"{CategoryEnum[product.type].value}{product.type}{product.brand}{product.model}{product.name}{product.material}{product.color_main}":
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
        return products

    async def get_suggestions(self, query: str):
        if not query:
            raise HTTPException(status_code=400, detail='Query is required')

        products_data = (
            await self.manager.execute(self.select_visible(
                self.Model.type,
                self.Model.name,
                self.Model.model,
                self.Model.brand).distinct())
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
        product_alias = aliased(self.Model)

        subquery = (
            select(
                product_alias.id,
                product_alias.memory,
                func.row_number().over(
                    partition_by=product_alias.memory,
                    order_by=case(
                        (product_alias.color_main == instance.color_main, 1),
                        else_=0
                    ).desc()
                ).label('row_num')
            )
            .where(
                product_alias.type == instance.type,
                product_alias.model == instance.model,
                product_alias.brand == instance.brand,
                product_alias.is_deleted == False
            )
            .subquery()
        )

        final_query = select(
            subquery.c.id,
            subquery.c.memory
        ).where(subquery.c.row_num == 1).order_by(subquery.c.memory)

        memory_variations_with_ids = (await self.manager.execute(final_query)).all()

        instance.memory_variations = [
            {
                'memory': row.memory,
                'id_product': row.id
            }
            for row in memory_variations_with_ids
        ]
        return instance

    async def get_color_variations(self, instance: Model) -> List:
        product_alias = aliased(self.Model)

        if not self.Model == Accessory:
            subquery = (
                select(
                    product_alias.id,
                    product_alias.color_main,
                    product_alias.color_hex,
                    product_alias.memory,
                    case(
                        (product_alias.memory == instance.memory, 1),
                        else_=0
                    ).label('preferred')
                )
                .where(
                    product_alias.type == instance.type,
                    product_alias.model == instance.model,
                    product_alias.brand == instance.brand,
                    product_alias.is_deleted == False,
                )
                .order_by(
                    product_alias.color_main,
                    product_alias.color_hex,
                    case(
                        (product_alias.memory == instance.memory, 1),
                        else_=0
                    ).desc()
                )
                .distinct(
                    product_alias.color_main,
                    product_alias.color_hex
                )
                .subquery()
            )

        else:
            subquery = (
                select(
                    product_alias.id,
                    product_alias.color_main,
                    product_alias.color_hex,
                )
                .where(
                    product_alias.type == instance.type,
                    product_alias.model == instance.model,
                    product_alias.brand == instance.brand,
                    product_alias.is_deleted == False
                )
                .order_by(
                    product_alias.color_main,
                    product_alias.color_hex,
                )
                .distinct(
                    product_alias.color_main,
                    product_alias.color_hex
                )
                .subquery()
            )

        final_query = select(
            subquery.c.color_main,
            subquery.c.color_hex,
            subquery.c.id
        )

        color_variations_with_ids = (await self.manager.execute(final_query)).all()

        instance.color_variations = [
            {
                'color_main': row.color_main,
                'color_hex': row.color_hex,
                'id_product': row.id
            }
            for row in color_variations_with_ids
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
        instance.photos = [photo for photo in instance.photos if not photo.is_banner]

        if not instance:
            raise HTTPException(status_code=404, detail="Такого товара не существует")

        await self.get_rating_and_reviews_count(instance)
        await self.get_reviews(instance)
        await self.get_color_variations(instance)
        instance.memory_variations = None
        if hasattr(instance, 'memory'):
            await self.get_memory_variations(instance)
        return instance

    async def get_instance(self, id_instance: int) -> Model:
        instance = (await self.manager.execute(
            self.select_visible()
            .options(selectinload(Product.photos))
            .where(self.Model.id == id_instance)
        )).scalars().first()
        instance.photos = [photo for photo in instance.photos if not photo.is_banner]
        return instance

    async def get_type_product(self, id_instance: int) -> Model:
        return await super().get(id_instance=id_instance)

    async def get(
            self,
            id_instance: int,
            is_auth: Optional[ServiceAuthenticate] = None,
            favourite_service: FavouriteService = None
    ) -> Model:
        product = await super().get(id_instance=id_instance)
        await self.get_rating_and_reviews_count(product)
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
        for product in result['items']:
            await self.get_rating_and_reviews_count(product)
        return result

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        products = (await self.manager.execute(
            query
            .limit(limit)
            .offset(offset)
            .options(selectinload(Product.photos)))
        ).scalars().all()
        for product in products:
            product.photos = [photo for photo in product.photos if not photo.is_banner]
        return products, (await self.manager.execute(query_count)).scalar()
