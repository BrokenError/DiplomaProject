from typing import Optional

from pydantic import BaseModel, Field

from apps.products.schemas import ProductCustom


class CartIn(BaseModel):
    id_product: int = Field(..., gt=0)

    class Config:
        orm_mode = True


class CartUpdate(BaseModel):
    quantity: int = Field(gt=0)

    class Config:
        orm_mode = True


class CartOut(BaseModel):
    id_product: int = Field()
    quantity: int = Field(gt=0)

    class Config:
        orm_mode = True


class CartShort(BaseModel):
    product: ProductCustom = Field()
    quantity: Optional[int] = Field(gte=0)

    class Config:
        orm_mode = True


class CartList(BaseModel):
    items: list[CartShort]

    class Config:
        orm_mode = True
