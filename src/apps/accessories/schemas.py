from typing import Optional

from pydantic import BaseModel, Field

from apps.products.schemas import ProductIn, ProductShort, ProductOut


class AccessoryIn(ProductIn):
    features: Optional[str] = Field(default="нет")


class AccessoryOut(ProductOut):
    features: Optional[str] = Field()


class AccessoryShort(ProductShort):
    ...


class AccessoryList(BaseModel):
    items: list[AccessoryShort]

    class Config:
        orm_mode = True
