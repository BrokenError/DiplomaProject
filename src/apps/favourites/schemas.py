from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.types import PositiveInt

from apps.products.schemas import ProductShort


class FavouriteIn(BaseModel):
    id_product: PositiveInt = Field()

    class Config:
        orm_mode = True


class FavouriteOut(BaseModel):
    id_product: PositiveInt = Field()

    class Config:
        orm_mode = True


class FavouriteDelete(BaseModel):
    id_product: PositiveInt = Field()
    id_user: PositiveInt = Field()


class FavouriteShort(BaseModel):
    product: Optional[ProductShort] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True


class FavouriteList(BaseModel):
    items: List[FavouriteShort]

    class Config:
        orm_mode = True
