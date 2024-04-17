from datetime import datetime, date, timedelta, time
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.json import timedelta_isoformat

from settings import settings_app


class UserIn(BaseModel):
    email: Optional[str] = Field()
    phone: Optional[str] = Field()

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


class UserOut(BaseModel):
    id: int = Field()
    email: str = Field()
    last_name: Optional[str] = Field()
    first_name: Optional[str] = Field()
    phone_number: Optional[str] = Field()
    is_deleted: bool = Field()
    date_created: datetime = Field()

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


class UserShort(BaseModel):
    ...


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field()
    last_name: Optional[str] = Field()


class TokenIn(BaseModel):
    token_access: Optional[str]
    token_refresh: Optional[str]


class TokenOut(BaseModel):
    token_access: Optional[str]
    token_refresh: Optional[str]


class UserAuthenticate(BaseModel):
    identifier: str
    code: int
