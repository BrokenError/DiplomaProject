from typing import Optional

from pydantic import Field

from apps.commons.basics.schemas import CameraIn, CameraOut
from apps.products.schemas import ProductShort, TechnicAdminSchema, TechnicOut, TechnicList
from field_names_ru import TabletFields


class TabletAdminSchema(TechnicAdminSchema, CameraIn):
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

    _validate_fields = TechnicAdminSchema.create_validator([
        'pixel_density',
        'processor_frequency',
        'number_cores',
        'accumulator_capacity'
    ], model_ru_fields=TabletFields)


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
