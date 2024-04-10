import logging
from typing import Optional

from apps.commons.services.base import ServiceBase
from apps.smartwatches.schemas import SmartwatchIn
from db.models import Smartwatch

logger = logging.getLogger('smartwatches')


class SmartwatchService(ServiceBase):
    Model = Smartwatch

    async def create(self, *, data: SmartwatchIn = None, data_extra: Optional[dict] = None) -> Model:
        smartwatch = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(smartwatch)
        return smartwatch
