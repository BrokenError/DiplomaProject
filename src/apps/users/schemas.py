from datetime import datetime, date, timedelta, time
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.json import timedelta_isoformat

from settings import settings_app


class UserIn(BaseModel):
    email: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    phone_number: str = Field()
    is_deleted: bool = Field(default=False)

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
    first_name: str = Field()
    last_name: str = Field()
    phone_number: str = Field()


class UserCreate(BaseModel):
    email: str
    password: str


class UserAuthenticate(BaseModel):
    email: str
    password: str


class TokensOut(BaseModel):
    access_token: str
    token_type: str
