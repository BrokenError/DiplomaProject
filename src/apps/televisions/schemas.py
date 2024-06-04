from typing import Optional

from pydantic import Field

from apps.products.schemas import ProductShort, TechnicAdminSchema, TechnicOut, TechnicList
from field_names_ru import TelevisionFields


class TelevisionAdminSchema(TechnicAdminSchema):
    consumption: int = Field()
    hdr_support: Optional[bool] = Field()
    angle_view: Optional[str] = Field()
    voice_assistant: Optional[str] = Field()
    wifi_availability: bool = Field(default=False)
    wifi_standard: Optional[str] = Field()
    sound_power: Optional[str] = Field()
    subwoofer: bool = Field(default=False)
    sound_surround: bool = Field(default=False)
    codecs: Optional[str] = Field()
    hdmi_ports: bool = Field(default=True)
    hdmi_version: Optional[str] = Field()
    usb_ports: Optional[str] = Field()
    smartphone_control: bool = Field(default=False)
    management_application: Optional[str] = Field()
    bluetooth_control: bool = Field(default=False)

    _validate_fields = TechnicAdminSchema.create_validator([
        'consumption',
    ], model_ru_fields=TelevisionFields)


class TelevisionOut(TechnicOut):
    consumption: int = Field()
    hdr_support: Optional[bool] = Field()
    angle_view: Optional[str] = Field()
    voice_assistant: Optional[str] = Field()
    wifi_availability: bool = Field()
    wifi_standard: Optional[str] = Field()
    sound_power: Optional[str] = Field()
    subwoofer: bool = Field()
    sound_surround: bool = Field()
    codecs: Optional[str] = Field()
    hdmi_ports: bool = Field()
    hdmi_version: Optional[str] = Field()
    usb_ports: Optional[str] = Field()
    smartphone_control: bool = Field()
    management_application: Optional[str] = Field()


class TelevisionShort(ProductShort):
    ...


class TelevisionList(TechnicList):
    items: list[TelevisionShort]
