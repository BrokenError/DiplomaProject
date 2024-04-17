from typing import Optional, List

from pydantic import BaseModel, Field

from apps.products.schemas import ProductPhoto


class OrderIn(BaseModel):
    description: Optional[str] = Field()
    status: str = Field(default="cart")

    class Config:
        orm_mode = True


class OrderItemIn(BaseModel):
    id_order: int = Field()
    id_user: int = Field()
    id_product: int = Field()
    quantity: int = Field(default=1)

    class Config:
        orm_mode = True


class OrderItemOut(BaseModel):
    product: ProductPhoto = Field()

    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: int = Field()
    description: Optional[str] = Field()
    status: str = Field()
    order_item: Optional[List[OrderItemOut]] = Field()

    class Config:
        orm_mode = True


class OrderShort(BaseModel):
    id: int = Field()
    description: Optional[str] = Field()
    status: str = Field()
    order_item: Optional[List[OrderItemOut]] = Field()

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    items: list[OrderShort]

    class Config:
        orm_mode = True
