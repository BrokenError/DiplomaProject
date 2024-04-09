import logging
from typing import Optional

from apps.commons.services.base import ServiceBase
from apps.smartphones.schemas import SmartphoneIn
from db.models import Smartphone

logger = logging.getLogger('smartphones')


class SmartphoneService(ServiceBase):
    Model = Smartphone

    async def create(self, *, data: SmartphoneIn = None, data_extra: Optional[dict] = None) -> Model:
        smartphone = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(smartphone)
        return smartphone
