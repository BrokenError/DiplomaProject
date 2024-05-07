from datetime import timedelta

from pydantic import BaseModel, Field
from pydantic.json import timedelta_isoformat


class CameraIn(BaseModel):
    number_cameras: int = Field()
    camera_quality: str = Field()
    video_format: str = Field()
    optical_stabilization: bool = Field()
    front_camera_quality: str = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class CameraOut(BaseModel):
    number_cameras: int = Field()
    camera_quality: str = Field()
    video_format: str = Field()
    optical_stabilization: bool = Field()
    front_camera_quality: str = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True
