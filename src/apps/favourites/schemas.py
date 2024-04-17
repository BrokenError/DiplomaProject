from pydantic import BaseModel, Field

from apps.products.schemas import ProductOut


class FavouriteIn(BaseModel):
    id_product: int = Field()

    class Config:
        orm_mode = True


class FavouriteDelete(BaseModel):
    id_product: int = Field()
    id_user: int = Field()


class FavouriteShort(BaseModel):
    id_product: int = Field()
    id_user: int = Field()

    class Config:
        orm_mode = True


class FavouriteList(BaseModel):
    items: list[FavouriteShort]

    class Config:
        orm_mode = True
