from datetime import datetime, date, timedelta, time
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.json import timedelta_isoformat

from apps.base.schemas import CameraIn, CameraOut
from apps.products.schemas import ProductIn, ProductOut, ProductShort
from settings import settings_app


class TabletIn(ProductIn, CameraIn):
    pixel_density: int = Field()
    degree_protection: str = Field()
    processor_model: str = Field()
    processor_frequency: int = Field()
    number_cores: int = Field()
    support_lte: bool = Field()
    sim_card_format: str = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()


class TabletOut(ProductOut, CameraOut):
    pixel_density: int = Field()
    degree_protection: str = Field()
    processor_model: str = Field()
    processor_frequency: int = Field()
    number_cores: int = Field()
    support_lte: bool = Field()
    sim_card_format: Optional[str] = Field()
    accumulator_type: Optional[str] = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()


class TabletShort(ProductShort):
    ...


class TabletList(BaseModel):
    items: list[TabletOut]

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
