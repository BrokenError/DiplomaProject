from datetime import datetime, date, timedelta, time
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field
from pydantic.json import timedelta_isoformat

from settings import settings_app


class ProductIn(BaseModel):
    date_created: datetime = Field(default=datetime.now())
    screen_type: str = Field()
    screen_diagonal: str = Field()
    screen_resolution: str = Field()
    screen_format: str = Field()
    model: str = Field()
    photos: list[str] = Field()
    operating_system: str = Field()
    matrix_frequency: int = Field()
    matrix_type: str = Field()
    matrix_brightness: str = Field()
    matrix_contrast: str = Field()
    sound_technology: str = Field()
    headphone_output: bool = Field()
    name: str = Field()
    color_main: str = Field()
    color_other: str = Field()
    material: str = Field()
    date_release: date = Field()
    memory_ram: int = Field()
    memory: int = Field()
    length: float = Field()
    width: float = Field()
    weight: float = Field()
    description: Optional[str] = Field()
    price: float = Field()
    id_provider: int = Field()
    is_active: bool = Field()
    quantity: int = Field()

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
    model: str = Field()

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
    date_created: datetime = Field()
    screen_type: str = Field()
    screen_diagonal: str = Field()
    screen_resolution: str = Field()
    screen_format: str = Field()
    model: str = Field()
    operating_system: str = Field()
    matrix_frequency: int = Field()
    matrix_type: str = Field()
    matrix_brightness: str = Field()
    matrix_contrast: str = Field()
    sound_technology: Optional[str] = Field()
    headphone_output: bool = Field()
    name: str = Field()
    color_main: str = Field()
    color_other: Optional[str] = Field()
    material: str = Field()
    date_release: date = Field()
    memory_ram: int = Field()
    memory: int = Field()
    length: float = Field()
    width: float = Field()
    weight: float = Field()
    description: Optional[str] = Field()
    price: float = Field()
    id_provider: Optional[int] = Field()
    is_active: bool = Field()
    quantity: int = Field()

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


class ProductList(BaseModel):
    items: list[ProductOut]

    class Config:
        orm_mode = True


class ProductDetail(BaseModel):
    items: ProductIn

    class Config:
        orm_mode = True
