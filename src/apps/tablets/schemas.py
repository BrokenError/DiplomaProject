from typing import Optional

from pydantic import Field

from apps.commons.basics.schemas import CameraIn, CameraOut
from apps.products.schemas import ProductShort, TechnicIn, TechnicOut, TechnicList


class TabletIn(TechnicIn, CameraIn):
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
    sensors: Optional[str] = Field()
    communicate_module: bool = Field(default=False)


class TabletOut(TechnicOut, CameraOut):
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
    sensors: Optional[str] = Field()
    communicate_module: bool = Field()


class TabletShort(ProductShort):
    ...


class TabletList(TechnicList):
    items: list[TabletShort]
