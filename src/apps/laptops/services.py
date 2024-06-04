import logging
from typing import Optional

from apps.laptops.schemas import LaptopAdminSchema
from apps.products.services import ProductService
from db.models import Laptop

logger = logging.getLogger('laptops')


class LaptopService(ProductService):
    Model = Laptop

    async def create(self, *, data: LaptopAdminSchema = None, data_extra: Optional[dict] = None) -> Model:
        laptop = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(laptop)
        return laptop
