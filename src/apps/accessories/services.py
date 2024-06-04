import logging
from typing import Optional

from apps.accessories.schemas import AccessoryAdminSchema
from apps.products.services import ProductService
from db.models import Accessory

logger = logging.getLogger('accessories')


class AccessoryService(ProductService):
    Model = Accessory

    async def create(self, *, data: AccessoryAdminSchema = None, data_extra: Optional[dict] = None) -> Model:
        accessory = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(accessory)
        return accessory
