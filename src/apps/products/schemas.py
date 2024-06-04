import re
from datetime import datetime, date
from enum import Enum
from typing import Optional, List, Any

from pydantic import BaseModel, PositiveInt, Field
from pydantic.class_validators import validator
from wtforms.validators import ValidationError

from apps.commons.basics.exceptions import validation_context
from apps.commons.pagination.schemas import MetaPage
from apps.reviews.schemas import ReviewCustom
from field_names_ru import ProductFields, TechnicsFields
from settings import settings_app


class PhotoOut(BaseModel):
    id: PositiveInt = Field()
    url: str = Field()

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    id: Optional[PositiveInt] = Field()
    name: Optional[str] = Field()
    price: Optional[float] = Field()
    photos: Optional[List[PhotoOut]] = Field()

    class Config:
        orm_mode = True

    @validator('photos', pre=True)
    def validate_photos(cls, value):
        if value:
            for photo in value:
                if not photo.url.startswith('http'):
                    photo.url = f"{settings_app.BASE_URL}{photo.url}"
            return value
        return None


class TypeEnum(Enum):
    television = "television"
    laptop = "laptop"
    tablet = "tablet"
    smartphone = "smartphone"
    smartwatch = "smartwatch"
    accessory = "accessory"


class ProductAdminSchema(BaseModel):
    date_created: datetime = Field(default=datetime.now())
    model: str = Field()
    brand: Optional[str] = Field()
    name: str = Field()
    type: str = Field()
    color_main: str = Field()
    color_hex: str = Field()
    material: str = Field()
    height: float = Field()
    width: float = Field()
    weight: float = Field()
    thickness: float = Field()
    description: Optional[str] = Field()
    price: float = Field()
    discount: Optional[int] = Field()
    id_provider: int = Field()
    is_active: bool = Field()
    quantity: int = Field()
    equipment: Optional[str] = Field()

    @classmethod
    def create_validator(cls, fields: List[str], model_ru_fields):
        @validator(*fields, pre=True, allow_reuse=True)
        def validate_fields(value, field: Any):
            with validation_context(
                    field=model_ru_fields[field.name],
                    detail=f"Значение должно быть больше нуля и длиной менее {settings_app.MAX_LENGTH_NUMBER}"
            ):
                if value is not None and (value < 1 or value and len(str(value)) >= settings_app.MAX_LENGTH_NUMBER):
                    raise ValueError()
            return value

        return validate_fields

    @validator('type', pre=True)
    def validate_type(cls, value, field: Any):
        with validation_context(
            field=ProductFields[field.name],
            detail=f"Возможные значения: {', '.join(CategoryEnum.__members__)}"
        ):
            TypeEnum(value)
        return value

    @validator('color_hex', pre=True)
    def validate_color_hex(cls, value, field: Any) -> str:
        with validation_context(
            field=ProductFields[field.name],
            detail=f"Формат данных: #XXXXXX"
        ):
            if not re.match(r'^#([A-Fa-f0-9]{6})$', value):
                raise ValidationError()
        return value

    @validator('discount', 'quantity', 'price', pre=True)
    def check_quantity(cls, value, field):
        with validation_context(
            field=field.name,
            detail="Значение должно быть не отрицательным"
        ):
            if value < 0:
                raise ValidationError()
        return value

    @validator('height', 'width', 'weight', 'thickness', pre=True)
    def validate_sizes(cls, value, field: Any) -> str:
        with validation_context(
                field=ProductFields[field.name],
                detail=f"Формат данных не должен превышать 6-и цифр: XXXX,XX"
        ):
            if len(str(value)) > 7:
                raise ValueError()
        return value

    @validator('color_main', 'brand', 'model', 'material', pre=True)
    def capitalize_strings(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.capitalize()
        return value

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        validate_assignment = True
        smart_union = True


class ProductCustom(ProductBase):
    discount: Optional[int] = Field()
    is_in_cart: Optional[bool] = Field(default=False)
    is_favourite: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True


class ProductCart(ProductCustom):
    quantity: int = Field(gte=0)


class ProductWithIdReview(ProductCustom):
    id_review: Optional[PositiveInt] = Field(default=None)


class ProductShort(ProductBase):
    discount: Optional[int] = Field()
    reviews_count: Optional[int] = Field()
    average_rating: Optional[float] = Field()
    is_favourite: Optional[bool] = Field(default=False)
    is_in_cart: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True


class ProductOut(ProductBase):
    date_created: datetime = Field(default=datetime.now())
    model: str = Field()
    brand: Optional[str] = Field()
    type: str = Field()
    color_main: str = Field()
    material: str = Field()
    height: float = Field()
    thickness: float = Field()
    width: float = Field()
    weight: float = Field()
    description: Optional[str] = Field()
    discount: Optional[int] = Field()
    id_provider: int = Field()
    is_active: bool = Field()
    quantity: int = Field()
    equipment: Optional[str] = Field()
    reviews_count: Optional[int] = Field()
    average_rating: Optional[float] = Field()
    is_favourite: Optional[bool] = Field()
    is_in_cart: Optional[bool] = Field(default=False)
    reviews: Optional[List[ReviewCustom]] = Field()
    color_variations: List[dict] = Field(default_factory=list)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True


class ProductType(BaseModel):
    id: PositiveInt = Field()
    type: str = Field()

    class Config:
        orm_mode = True


class ProductList(BaseModel):
    items: List[ProductShort]
    meta: MetaPage

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True


class ProductDetail(BaseModel):
    items: ProductAdminSchema

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True


class TechnicAdminSchema(ProductAdminSchema):
    date_release: date = Field()
    screen_diagonal: int = Field()
    screen_resolution: str = Field()
    screen_format: str = Field()
    operating_system: str = Field()
    matrix_frequency: int = Field()
    matrix_type: str = Field()
    matrix_brightness: str = Field()
    matrix_contrast: str = Field()
    sound_technology: str = Field()
    headphone_output: bool = Field()
    color_other: Optional[str] = Field()
    memory_ram: Optional[int] = Field()
    memory: Optional[int] = Field()

    _validate_fields = ProductAdminSchema.create_validator([
        'matrix_frequency',
        'memory_ram',
        'memory',
        'screen_diagonal'
    ], model_ru_fields=TechnicsFields)


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
    color_other: Optional[str] = Field()
    memory_ram: int = Field()
    memory: int = Field()
    reviews: List[ReviewCustom] = Field(default_factory=list)
    memory_variations: dict = Field(default_factory=dict)


class TechnicList(ProductList):
    items: List[TechnicOut]


class ProductPhoto(ProductBase):
    discount: Optional[str] = Field()


class SuggestionOut(BaseModel):
    suggestions: Optional[List[str]] = Field(default=None)

    class Config:
        orm_mode = True


class CategoryEnum(str, Enum):
    television = "телевизор"
    laptop = "ноутбук"
    tablet = "планшет"
    smartphone = "смартфон"
    smartwatch = "часы"
    accessory = "аксессуар"
