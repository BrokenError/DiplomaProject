from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import PositiveInt

from apps.products.schemas import ProductCart


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
    id: PositiveInt = Field()
    product: ProductCart = Field()
    quantity: Optional[int] = Field(gte=0)

    class Config:
        orm_mode = True


class CartList(BaseModel):
    items: list[CartShort]

    class Config:
        orm_mode = True


class CartPayment(BaseModel):
    cart_number: Optional[PositiveInt] = Field()
    cart_date_expires: Optional[datetime] = Field()
    cart_pin: Optional[PositiveInt] = Field()

    class Config:
        orm_mode = True
