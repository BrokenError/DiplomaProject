import logging
import os
from functools import lru_cache
from logging.config import dictConfig
from pathlib import Path

from fastapi_storages import FileSystemStorage
from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings

_NAME_SERVICE_DEFAULT = "techzone"

BASE_PATH = Path(__file__).parent.resolve()


logging.config.fileConfig(
    os.path.join(os.path.dirname(__file__), 'logging.conf'),
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


class SettingsApp(BaseSettings):
    COMPANY_USERNAME_ADMIN = ''
    COMPANY_PASSWORD_ADMIN = ''
    BASE_URL = ''
    CATEGORIES: str = ''
    URL_ADMIN = ''
    PATH_STORAGE_BASE = FileSystemStorage(path="/media")
    PATH_STORAGE_USER = FileSystemStorage(path='../techzone/media/users')
    NAME_SERVICE: str = _NAME_SERVICE_DEFAULT
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8001
    SMTP_SERVER = ''
    SMTP_PORT = 0
    SMTP_USERNAME = ''
    SMTP_PASSWORD = ''
    EMAIL_REGEX = ''
    PHONE_REGEX = ''
    SECRET_KEY = ''
    ALGORITHM = ''
    ACCESS_TOKEN_EXPIRE_MINUTES = 0
    COMPANY_NAME = ''

    IS_DEBUG: bool = False

    TZ: str = 'Europe/Moscow'

    @validator('CATEGORIES')
    def validate_categories(cls, value: str):
        if isinstance(value, tuple):
            return value
        return value.split(', ')

    class Config:
        env_file = '../.env'


@lru_cache
def get_settings_app() -> SettingsApp:
    return SettingsApp()


settings_app = get_settings_app()
