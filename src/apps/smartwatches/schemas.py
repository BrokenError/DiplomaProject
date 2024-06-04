from typing import Optional

from pydantic import Field

from apps.products.schemas import ProductShort, TechnicAdminSchema, TechnicOut, TechnicList
from field_names_ru import SmartwatchFields


class SmartwatchAdminSchema(TechnicAdminSchema):
    material_belt: str = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()
    water_resistance: Optional[int] = Field()
    measurements: Optional[str] = Field()

    _validate_fields = TechnicAdminSchema.create_validator([
        'pixel_density',
        'water_resistance',
        'accumulator_capacity',
    ], model_ru_fields=SmartwatchFields)


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
