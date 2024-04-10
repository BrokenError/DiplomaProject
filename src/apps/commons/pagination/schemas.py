from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class MetaPage(BaseModel):
    count_objects: int = Field(alias='objectsCount')
    number_page: int = Field(alias='pageNumber')
    size_page: int = Field(alias='pageSize')
    total_objects: int = Field(alias='objectsTotal')
    total_pages: int = Field(alias='pagesTotal')

    class Config:
        allow_population_by_field_name = True


class Pagination(BaseModel):
    size_page: Optional[int] = Field(default=20, alias='pageSize')
    number_page: PositiveInt = Field(default=1, alias='pageNumber')

    class Config:
        allow_population_by_field_name = True
