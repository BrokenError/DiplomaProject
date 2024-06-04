from typing import Optional

from pydantic import BaseModel, Field

from apps.commons.pagination.schemas import MetaPage
from apps.products.schemas import ProductAdminSchema, ProductShort, ProductOut


class AccessoryAdminSchema(ProductAdminSchema):
    features: Optional[str] = Field()


class AccessoryOut(ProductOut):
    features: Optional[str] = Field()


class AccessoryShort(ProductShort):
    ...


class AccessoryList(BaseModel):
    items: list[AccessoryShort]
    meta: MetaPage

    class Config:
        orm_mode = True
