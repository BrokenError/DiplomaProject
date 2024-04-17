from typing import Optional

from pydantic import Field

from apps.products.schemas import ProductShort, TechnicOut, TechnicIn, TechnicList


class LaptopIn(TechnicIn):
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
    microphone: Optional[bool] = Field(default=True)


class LaptopOut(TechnicOut):
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
    microphone: Optional[bool] = Field()


class LaptopShort(ProductShort):
    ...


class LaptopList(TechnicList):
    items: list[LaptopShort]
