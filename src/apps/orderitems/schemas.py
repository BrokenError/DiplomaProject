from pydantic import BaseModel, Field


class OrderItemIn(BaseModel):
    id_user: int = Field()
    id_product: int = Field()


class OrderItemOut(BaseModel):
    id: int = Field()
    id_order: int = Field()
    id_user: int = Field()
    id_product: int = Field()
