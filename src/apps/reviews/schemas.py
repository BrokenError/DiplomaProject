from datetime import datetime, time, date, timedelta
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.json import timedelta_isoformat

from settings import settings_app


class ReviewOut(BaseModel):
    user: str = Field()
    rating: int = Field(gt=0)
    text: Optional[str] = Field()
    date_created: Optional[datetime] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.strftime(settings_app.FORMAT_DATETIME),
            date: lambda v: v.strftime(settings_app.FORMAT_DATE),
            time: lambda v: v.strftime(settings_app.FORMAT_TIME),
            timedelta: timedelta_isoformat,
        }
        smart_union = True
