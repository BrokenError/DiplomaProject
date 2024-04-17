import logging
from typing import Optional

from apps.products.services import ProductService
from apps.smartphones.schemas import SmartphoneIn
from db.models import Smartphone

logger = logging.getLogger('smartphones')


class SmartphoneService(ProductService):
    Model = Smartphone

    async def create(self, *, data: SmartphoneIn = None, data_extra: Optional[dict] = None) -> Model:
        smartphone = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(smartphone)
        return smartphone
