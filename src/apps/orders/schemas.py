
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.schema import datetime
from pydantic.types import PositiveInt

from apps.products.schemas import ProductPhoto


class OrderStatus(str, Enum):
    CART = 'cart'
    ASSEMBLY = 'assembly'
    READY = 'ready'
    GOT = 'got'


class OrderPayment(str, Enum):
    CASH = 'cash'
    CARD = 'card'


class OrderIn(BaseModel):
    ids_order_items: List[PositiveInt]
    payment_method: OrderPayment

    class Config:
        orm_mode = True


class OrderItemOut(BaseModel):
    id: PositiveInt = Field()
    product: ProductPhoto = Field()
    quantity: PositiveInt = Field()

    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: PositiveInt = Field()
    payment_method: str = Field()
    date_created: Optional[datetime] = Field()
    status: str = Field()
    is_paid: bool = Field()

    class Config:
        orm_mode = True


class OrderShort(BaseModel):
    id: PositiveInt = Field()
    description: Optional[str] = Field()
    status: str = Field()
    date_created: Optional[datetime] = Field()
    order_items: Optional[List[OrderItemOut]] = Field()

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    items: list[OrderShort]

    class Config:
        orm_mode = True
