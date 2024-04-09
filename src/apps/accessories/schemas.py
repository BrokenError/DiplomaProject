from typing import Optional

from pydantic import BaseModel, Field

from apps.products.schemas import ProductIn, ProductShort, ProductOut


class AccessoryIn(ProductIn):
    color: str = Field()
    degree_protection: str = Field()


class AccessoryOut(ProductOut):
    color: Optional[str] = Field()
    degree_protection: str = Field()


class AccessoryShort(ProductShort):
    ...


class AccessoryList(BaseModel):
    items: list[AccessoryOut]

    class Config:
        orm_mode = True
