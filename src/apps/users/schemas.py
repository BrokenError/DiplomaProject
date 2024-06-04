import re
from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field
from pydantic.class_validators import validator

from apps.commons.basics.exceptions import validation_context
from field_names_ru import UserFields
from settings import settings_app


class UserIn(BaseModel):
    email: Optional[str] = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True


class UserAdminSchema(BaseModel):
    email: str = Field
    first_name: Optional[str] = Field()
    last_name: Optional[str] = Field()
    phone_number: Optional[str] = Field()
    photo_url: Optional[UploadFile] = Field(None)

    @validator("email", pre=True)
    def validate_email(cls, value, field) -> str:
        with validation_context(
                field=UserFields[field.name],
                detail="Пример правильного формата данных: test@gmail.com"
        ):
            if not re.match(settings_app.EMAIL_REGEX, value):
                raise ValueError()
        return value

    @validator("phone_number", pre=True)
    def validate_phone_number(cls, value, field) -> Optional[str]:
        with validation_context(
            field=UserFields[field.name],
            detail="Пример правильного формата данных: 89999999999"
        ):
            if not re.match(settings_app.PHONE_REGEX, value):
                raise ValueError()
        return value

    class Config:
        orm_mode = True


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
        smart_union = True

    @validator("photo_url", pre=True)
    def add_base_url(cls, value):
        if value:
            return f"{settings_app.BASE_URL}{value}"
        return None


class UserShort(BaseModel):
    ...


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field()
    last_name: Optional[str] = Field()
    phone_number: Optional[str] = Field()
    photo_url: Optional[str] = Field(None, init=False)

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
