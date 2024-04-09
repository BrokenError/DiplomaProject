from functools import lru_cache

from pydantic import BaseSettings

from settings import _NAME_SERVICE_DEFAULT


class SettingsDB(BaseSettings):
    DB_HOST: str = 'db_techzone'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = _NAME_SERVICE_DEFAULT
    DB_USER: str = _NAME_SERVICE_DEFAULT
    DB_PORT: str = '5432'


@lru_cache
def get_settings_db() -> SettingsDB:
    return SettingsDB()


settings_db = get_settings_db()
