
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.types import PositiveInt

from apps.products.schemas import ProductPhoto


class OrderStatus(str, Enum):
    CART = 'cart'
    ASSEMBLY = 'assembly'
    READY = 'ready'
    GOT = 'got'


class OrderIn(BaseModel):
    order_items: List[PositiveInt]
    description: Optional[str] = Field()
    status: OrderStatus

    class Config:
        orm_mode = True


class OrderItemOut(BaseModel):
    product: ProductPhoto = Field()

    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: PositiveInt = Field()
    description: Optional[str] = Field()
    status: str = Field()
    order_item: Optional[List[OrderItemOut]] = Field()

    class Config:
        orm_mode = True


class OrderShort(BaseModel):
    id: PositiveInt = Field()
    description: Optional[str] = Field()
    status: str = Field()
    order_item: Optional[List[OrderItemOut]] = Field()

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    items: list[OrderShort]

    class Config:
        orm_mode = True
