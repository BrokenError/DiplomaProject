from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

_NAME_SERVICE_DEFAULT = "techzone"

BASE_PATH = Path(__file__).parent.resolve()


class SettingsApp(BaseSettings):
    COMPANY_USERNAME_ADMIN = ''
    COMPANY_PASSWORD_ADMIN = ''
    URL_ADMIN = ''
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
    FORMAT_DATETIME: str
    FORMAT_DATE: str
    FORMAT_TIME: str = "%H:%M:%S"

    IS_DEBUG: bool = False

    TZ: str = 'Europe/Moscow'

    PATH_STORAGE_FILE: str = ""

    class Config:
        env_file = '../.env'


@lru_cache
def get_settings_app() -> SettingsApp:
    return SettingsApp()


settings_app = get_settings_app()
