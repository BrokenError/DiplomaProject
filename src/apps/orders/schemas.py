
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.class_validators import validator
from pydantic.schema import datetime
from pydantic.types import PositiveInt

from apps.commons.basics.exceptions import validation_context
from apps.products.schemas import ProductWithIdReview
from field_names_ru import OrderFields


class OrderStatus(str, Enum):
    cart = 'cart'
    assembly = 'assembly'
    ready = 'ready'
    got = 'got'


class OrderPayment(str, Enum):
    cash = 'cash'
    card = 'card'


class OrderIn(BaseModel):
    ids_order_items: List[PositiveInt]
    cost: float = Field()
    payment_method: OrderPayment

    class Config:
        orm_mode = True


class OrderAdminSchema(BaseModel):
    user: str = Field()
    status: OrderStatus = Field()
    payment_method: OrderPayment = Field()
    is_paid: bool = Field(default=False)

    @validator('payment_method', pre=True)
    def validate_payment_method(cls, value, field):
        with validation_context(
            field=OrderFields[field.name],
            detail=f"Возможные значения: {', '.join(OrderPayment.__members__)}"
        ):
            OrderPayment(value)
        return value

    @validator('status', pre=True)
    def validate_status(cls, value, field):
        with validation_context(
            field=OrderFields[field.name],
            detail=f"Возможные значения: {', '.join(OrderStatus.__members__)}"
        ):
            OrderStatus(value)
        return value

    class Config:
        orm_mode = True


class OrderItemOut(BaseModel):
    id: PositiveInt = Field()
    product: ProductWithIdReview = Field()
    quantity: PositiveInt = Field()

    class Config:
        orm_mode = True


class OrderItemShort(BaseModel):
    id: PositiveInt = Field()
    product: ProductWithIdReview = Field()
    quantity: PositiveInt = Field()

    class Config:
        orm_mode = True


class OrderPaymentOut(BaseModel):
    url: Optional[str] = Field()


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
    payment_method: Optional[str] = Field()
    status: str = Field()
    date_created: Optional[datetime] = Field()
    order_items: Optional[List[OrderItemShort]] = Field()

    class Config:
        orm_mode = True


class OrderCustom(BaseModel):
    id: PositiveInt = Field()
    payment_method: Optional[str] = Field()
    status: str = Field()
    date_created: Optional[datetime] = Field()
    order_items: Optional[List[OrderItemOut]] = Field()

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    items: list[OrderShort]

    class Config:
        orm_mode = True
