from datetime import datetime, date, timedelta, time
from typing import Optional, List

from pydantic import BaseModel, PositiveInt, Field
from pydantic.json import timedelta_isoformat

from apps.reviews.schemas import ReviewOut
from settings import settings_app


class PhotoOut(BaseModel):
    id: int
    url: str

    class Config:
        orm_mode = True


class ProductIn(BaseModel):
    date_created: datetime = Field(default=datetime.now())
    model: str = Field()
    name: str = Field()
    type: str = Field()
    color_main: str = Field()
    material: str = Field()
    length: float = Field()
    width: float = Field()
    weight: float = Field()
    description: Optional[str] = Field()
    price: float = Field()
    discount: Optional[int] = Field()
    id_provider: int = Field()
    is_active: bool = Field()
    quantity: int = Field()
    equipment: Optional[str] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.strftime(settings_app.FORMAT_DATETIME),
            date: lambda v: v.strftime(settings_app.FORMAT_DATE),
            time: lambda v: v.strftime(settings_app.FORMAT_TIME),
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class ProductShort(BaseModel):
    id: PositiveInt = Field()
    name: Optional[str] = Field()
    price: Optional[float] = Field()
    discount: Optional[int] = Field()
    photos: Optional[List[PhotoOut]] = Field()
    reviews_count: Optional[int] = Field()
    average_rating: Optional[float] = Field()
    is_favourite: Optional[bool] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.strftime(settings_app.FORMAT_DATETIME),
            date: lambda v: v.strftime(settings_app.FORMAT_DATE),
            time: lambda v: v.strftime(settings_app.FORMAT_TIME),
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class ProductOut(BaseModel):
    id: PositiveInt = Field()
    date_created: datetime = Field(default=datetime.now())
    model: str = Field()
    name: str = Field()
    type: str = Field()
    color_main: str = Field()
    material: str = Field()
    height: float = Field()
    thickness: float = Field()
    width: float = Field()
    weight: float = Field()
    description: Optional[str] = Field()
    price: float = Field()
    discount: Optional[int] = Field()
    id_provider: int = Field()
    is_active: bool = Field()
    quantity: int = Field()
    equipment: Optional[str] = Field()
    photos: Optional[List[PhotoOut]] = Field()
    reviews_count: Optional[int] = Field()
    average_rating: Optional[float] = Field()
    is_favourite: Optional[bool] = Field()
    reviews: Optional[List[ReviewOut]] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.strftime(settings_app.FORMAT_DATETIME),
            date: lambda v: v.strftime(settings_app.FORMAT_DATE),
            time: lambda v: v.strftime(settings_app.FORMAT_TIME),
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class ProductType(BaseModel):
    id: int = Field()
    type: str = Field()

    class Config:
        orm_mode = True


class ProductList(BaseModel):
    items: List[ProductShort]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.strftime(settings_app.FORMAT_DATETIME),
            date: lambda v: v.strftime(settings_app.FORMAT_DATE),
            time: lambda v: v.strftime(settings_app.FORMAT_TIME),
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class ProductDetail(BaseModel):
    items: ProductIn

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.strftime(settings_app.FORMAT_DATETIME),
            date: lambda v: v.strftime(settings_app.FORMAT_DATE),
            time: lambda v: v.strftime(settings_app.FORMAT_TIME),
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class TechnicIn(ProductIn):
    date_release: date = Field()
    screen_type: str = Field()
    screen_diagonal: str = Field()
    screen_resolution: str = Field()
    screen_format: str = Field()
    operating_system: str = Field()
    matrix_frequency: int = Field()
    matrix_type: str = Field()
    matrix_brightness: str = Field()
    matrix_contrast: str = Field()
    sound_technology: str = Field()
    headphone_output: bool = Field()
    color_other: str = Field()
    memory_ram: int = Field()
    memory: int = Field()


class TechnicOut(ProductOut):
    date_release: date = Field()
    screen_type: str = Field()
    screen_diagonal: str = Field()
    screen_resolution: str = Field()
    screen_format: str = Field()
    operating_system: str = Field()
    matrix_frequency: int = Field()
    matrix_type: str = Field()
    matrix_brightness: str = Field()
    matrix_contrast: str = Field()
    sound_technology: str = Field()
    headphone_output: bool = Field()
    color_other: str = Field()
    memory_ram: int = Field()
    memory: int = Field()
    reviews: List[ReviewOut] = Field(default_factory=list)


class TechnicList(ProductList):
    items: List[TechnicOut]


class ProductPhoto(BaseModel):
    name: Optional[str] = Field()
    price: Optional[float] = Field()
    discount: Optional[str] = Field()
    photos: Optional[List[PhotoOut]] = Field()

    class Config:
        orm_mode = True
