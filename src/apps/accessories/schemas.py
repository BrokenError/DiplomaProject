from typing import Optional

from pydantic import BaseModel, Field

from apps.commons.pagination.schemas import MetaPage
from apps.products.schemas import ProductIn, ProductShort, ProductOut


class AccessoryIn(ProductIn):
    features: Optional[str] = Field(default="нет")


class AccessoryOut(ProductOut):
    features: Optional[str] = Field()


class AccessoryShort(ProductShort):
    ...


class AccessoryList(BaseModel):
    items: list[AccessoryShort]
    meta: MetaPage

    class Config:
        orm_mode = True
