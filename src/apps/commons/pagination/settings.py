from functools import lru_cache

from pydantic import BaseSettings


class SettingsPagination(BaseSettings):
    SIZE_PAGE: int = 20


@lru_cache
def get_settings_pagination() -> SettingsPagination:
    return SettingsPagination()


settings_pagination = get_settings_pagination()
