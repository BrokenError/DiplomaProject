import logging
from typing import Optional

from apps.commons.services.base import ServiceBase
from apps.tablets.schemas import TabletIn
from db.models import Tablet

logger = logging.getLogger('tablets')


class TabletService(ServiceBase):
    Model = Tablet

    async def create(self, *, data: TabletIn = None, data_extra: Optional[dict] = None) -> Model:
        tablet = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(tablet)
        return tablet
