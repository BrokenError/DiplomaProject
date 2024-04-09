from pydantic import BaseModel, Field

from apps.products.schemas import ProductIn, ProductOut, ProductShort


class SmartwatchIn(ProductIn):
    material_belt: str = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()


class SmartwatchOut(ProductOut):
    material_belt: str = Field()
    pixel_density: int = Field()
    degree_protection: str = Field()
    accumulator_type: str = Field()
    accumulator_capacity: int = Field()
    fast_charge: bool = Field()


class SmartwatchShort(ProductShort):
    ...


class SmartwatchList(BaseModel):
    items: list[SmartwatchOut]

    class Config:
        orm_mode = True
