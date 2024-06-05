from typing import Optional

from pydantic import Field

from apps.commons.basics.schemas import CameraOut, CameraIn
from apps.products.schemas import ProductShort, TechnicAdminSchema, TechnicOut, TechnicList
from field_names_ru import SmartphoneFields


class SmartphoneAdminSchema(TechnicAdminSchema, CameraIn):
    support_lte: bool = Field()
    sim_card_format: str = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    processor_model: str = Field()
    processor_frequency: float = Field()
    number_cores: int = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()
    communication_standard: Optional[str] = Field()
    sim_card_number: Optional[str] = Field()
    sensors: Optional[str] = Field()

    _validate_fields = TechnicAdminSchema.create_validator([
        'pixel_density',
        'processor_frequency',
        'number_cores',
        'accumulator_capacity',
    ], model_ru_fields=SmartphoneFields)


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
