from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.class_validators import validator
from pydantic.types import PositiveInt

from settings import settings_app


class ReviewIn(BaseModel):
    rating: PositiveInt = Field()
    text: Optional[str] = Field()

    class Config:
        orm_mode = True


class ReviewCustom(BaseModel):
    user: Optional[str] = Field(default=None)
    photo_url: Optional[str] = Field()
    rating: PositiveInt = Field()
    text: Optional[str] = Field()
    date_created: Optional[datetime] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True

    @validator("photo_url", pre=True)
    def add_base_url(cls, value):
        if value:
            return f"{settings_app.BASE_URL}{value}"
        return None


class ReviewOut(BaseModel):
    id: PositiveInt = Field()
    id_product: PositiveInt = Field()
    id_user: PositiveInt = Field()
    rating: PositiveInt = Field()
    text: Optional[str] = Field()
    date_created: Optional[datetime] = Field()

    class Config:
        orm_mode = True


class ReviewUpdate(BaseModel):
    rating: Optional[PositiveInt] = Field()
    text: Optional[str] = Field()

    class Config:
        orm_mode = True