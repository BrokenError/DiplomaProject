import logging
from typing import Optional

from apps.products.services import ProductService
from apps.televisions.schemas import TelevisionAdminSchema
from db.models import Television

logger = logging.getLogger('televisions')


class TelevisionService(ProductService):
    Model = Television

    async def create(self, *, data: TelevisionAdminSchema = None, data_extra: Optional[dict] = None) -> Model:
        television = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(television)
        return television
