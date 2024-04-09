import logging
from typing import Optional

from apps.commons.services.base import ServiceBase
from apps.laptops.schemas import LaptopIn
from db.models import Laptop

logger = logging.getLogger('events')


class LaptopService(ServiceBase):
    Model = Laptop

    async def create(self, *, data: LaptopIn = None, data_extra: Optional[dict] = None) -> Model:
        laptop = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(laptop)
        return laptop
