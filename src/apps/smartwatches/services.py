import logging
from typing import Optional

from apps.products.services import ProductService
from apps.smartwatches.schemas import SmartwatchAdminSchema
from db.models import Smartwatch

logger = logging.getLogger('smartwatches')


class SmartwatchService(ProductService):
    Model = Smartwatch

    async def create(self, *, data: SmartwatchAdminSchema = None, data_extra: Optional[dict] = None) -> Model:
        smartwatch = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(smartwatch)
        return smartwatch
