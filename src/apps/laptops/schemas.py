from typing import Optional

from pydantic import BaseModel, Field

from apps.products.schemas import ProductIn, ProductOut, ProductShort


class LaptopIn(ProductIn):
    consumption: int = Field()
    keyboard_layout: str = Field()
    keyboard_backlight: str = Field()
    touchpad: str = Field()
    fingerprint_scanner: bool = Field()
    hdr_support: Optional[bool] = Field()
    type_graphics_accelerator: str = Field()
    video_card_model: str = Field()
    discrete_graphics: Optional[str] = Field()
    video_chip: str = Field()
    video_memory_type: Optional[str] = Field()
    video_memory: int = Field()
    clock_speed: int = Field()
    voice_assistant: Optional[str] = Field()
    wifi_availability: bool = Field()
    wifi_standard: Optional[str] = Field()
    sound_power: Optional[str] = Field()
    hdmi_ports: bool = Field()
    usb_devices: Optional[str] = Field()
    battery_life: float = Field()


class LaptopOut(ProductOut):
    consumption: int = Field()
    keyboard_layout: str = Field()
    keyboard_backlight: str = Field()
    touchpad: str = Field()
    fingerprint_scanner: bool = Field()
    hdr_support: Optional[bool] = Field()
    type_graphics_accelerator: str = Field()
    video_card_model: str = Field()
    discrete_graphics: Optional[str] = Field()
    video_chip: str = Field()
    video_memory_type: Optional[str] = Field()
    video_memory: int = Field()
    clock_speed: int = Field()
    voice_assistant: Optional[str] = Field()
    wifi_availability: bool = Field()
    wifi_standard: Optional[str] = Field()
    sound_power: Optional[str] = Field()
    hdmi_ports: bool = Field()
    usb_devices: Optional[str] = Field()
    battery_life: float = Field()


class LaptopShort(ProductShort):
    ...


class LaptopList(BaseModel):
    items: list[LaptopOut]

    class Config:
        orm_mode = True
