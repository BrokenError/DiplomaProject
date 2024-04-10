from typing import Optional

from pydantic import BaseModel, Field

from apps.base.schemas import CameraOut, CameraIn
from apps.products.schemas import ProductIn, ProductOut, ProductShort


class SmartphoneIn(ProductIn, CameraIn):
    support_lte: bool = Field()
    sim_card_format: str = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    processor_model: str = Field()
    processor_frequency: int = Field()
    number_cores: int = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()


class SmartphoneOut(ProductOut, CameraOut):
    support_lte: bool = Field()
    sim_card_format: Optional[str] = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    processor_model: str = Field()
    processor_frequency: Optional[int] = Field()
    number_cores: int = Field()
    accumulator_type: Optional[str] = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()


class SmartphoneShort(ProductShort):
    ...


class SmartphoneList(BaseModel):
    items: list[SmartphoneOut]

    class Config:
        orm_mode = True
