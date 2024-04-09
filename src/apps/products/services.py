import logging
from typing import Optional

from sqlalchemy.sql import crud

from apps.commons.pagination.schemas import Pagination
from apps.commons.services.base import ServiceBase
from apps.products.schemas import ProductIn
from db.models import Product

logger = logging.getLogger('products')


class ProductService(ServiceBase):
    Model = Product

    async def create(self, *, data: ProductIn = None, data_extra: Optional[dict] = None) -> Model:
        product = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(product)
        return product
