import logging
from typing import Optional

from apps.commons.services.base import ServiceBase
from apps.orderitems.schemas import OrderItemIn
from db.models import OrderItem

logger = logging.getLogger('orderitems')


class OrderItemService(ServiceBase):
    Model = OrderItem

    async def create(self, *, data: OrderItemIn = None, data_extra: Optional[dict] = None) -> Model:
        laptop = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(laptop)
        return laptop
