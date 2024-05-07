from datetime import datetime, date, timedelta
from typing import Optional, List

from pydantic import BaseModel, PositiveInt, Field
from pydantic.json import timedelta_isoformat

from apps.reviews.schemas import ReviewOut


class PhotoOut(BaseModel):
    id: PositiveInt = Field()
    url: str = Field()

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
    discount: Optional[int] = Field(gte=0)
    id_provider: PositiveInt = Field()
    is_active: bool = Field()
    quantity: int = Field(gte=0)
    equipment: Optional[str] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class ProductCustom(BaseModel):
    id: Optional[PositiveInt] = Field()
    name: Optional[str] = Field()
    price: Optional[float] = Field()
    discount: Optional[int] = Field()
    photos: Optional[List[PhotoOut]] = Field()
    is_favourite: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True


class ProductShort(BaseModel):
    id: PositiveInt = Field()
    name: Optional[str] = Field()
    price: Optional[float] = Field()
    discount: Optional[int] = Field()
    photos: Optional[List[PhotoOut]] = Field()
    reviews_count: Optional[int] = Field()
    average_rating: Optional[float] = Field()
    is_favourite: Optional[bool] = Field()
    is_in_cart: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
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
    is_in_cart: Optional[bool] = Field(default=False)
    reviews: Optional[List[ReviewOut]] = Field()
    color_variations: List[dict] = Field(default_factory=list)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class ProductType(BaseModel):
    id: PositiveInt = Field()
    type: str = Field()

    class Config:
        orm_mode = True


class ProductList(BaseModel):
    items: List[ProductShort]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class ProductDetail(BaseModel):
    items: ProductIn

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class TechnicIn(ProductIn):
    date_release: date = Field()
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
    memory_ram: Optional[PositiveInt] = Field()
    memory: Optional[PositiveInt] = Field()


class TechnicOut(ProductOut):
    date_release: date = Field()
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
    memory_variations: List[PositiveInt] = Field(default_factory=list)


class TechnicList(ProductList):
    items: List[TechnicOut]


class ProductPhoto(BaseModel):
    id: PositiveInt = Field()
    name: Optional[str] = Field()
    price: Optional[float] = Field()
    discount: Optional[str] = Field()
    photos: Optional[List[PhotoOut]] = Field()

    class Config:
        orm_mode = True
