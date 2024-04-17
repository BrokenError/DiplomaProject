from typing import Optional

from pydantic import Field

from apps.commons.basics.schemas import CameraOut, CameraIn
from apps.products.schemas import ProductShort, TechnicIn, TechnicOut, TechnicList


class SmartphoneIn(TechnicIn, CameraIn):
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
    communication_standard: Optional[str] = Field()
    sim_card_number: Optional[str] = Field()
    sensors: Optional[str] = Field()


class SmartphoneOut(TechnicOut, CameraOut):
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
    communication_standard: Optional[str] = Field()
    sim_card_number: Optional[str] = Field()
    sensors: Optional[str] = Field()


class SmartphoneShort(ProductShort):
    ...


class SmartphoneList(TechnicList):
    items: list[SmartphoneShort]
