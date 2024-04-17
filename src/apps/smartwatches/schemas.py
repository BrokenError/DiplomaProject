from typing import Optional

from pydantic import Field

from apps.products.schemas import ProductShort, TechnicIn, TechnicOut, TechnicList


class SmartwatchIn(TechnicIn):
    material_belt: str = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()
    water_resistance: Optional[int] = Field()
    measurements: Optional[str] = Field()


class SmartwatchOut(TechnicOut):
    material_belt: str = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()
    water_resistance: Optional[int] = Field()
    measurements: Optional[str] = Field()


class SmartwatchShort(ProductShort):
    ...


class SmartwatchList(TechnicList):
    items: list[SmartwatchShort]
