from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.json import timedelta_isoformat


class UserIn(BaseModel):
    email: Optional[str] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class UserOut(BaseModel):
    id: int = Field()
    email: str = Field()
    last_name: Optional[str] = Field()
    photo_url: Optional[str] = Field()
    first_name: Optional[str] = Field()
    phone_number: Optional[str] = Field()
    date_created: datetime = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            timedelta: timedelta_isoformat,
        }
        smart_union = True


class UserShort(BaseModel):
    ...


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field()
    last_name: Optional[str] = Field()
    phone_number: Optional[str] = Field()
    photo_url: Optional[str] = Field()

    class Config:
        orm_mode = True


class TokenIn(BaseModel):
    token_refresh: Optional[str]


class TokenOut(BaseModel):
    token_access: Optional[str]
    token_refresh: Optional[str]


class UserAuthenticate(BaseModel):
    email: str
    code: int
