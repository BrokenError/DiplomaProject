from typing import Optional

from fastapi import Query

from apps.commons.pagination.schemas import Pagination, MetaPage
from apps.commons.pagination.settings import settings_pagination


def get_pagination(
        size_page: Optional[int] = Query(
            default=settings_pagination.SIZE_PAGE,
            title='Размер страницы',
            description=f'По умолчанию {settings_pagination.SIZE_PAGE}'
        ),
        number_page: Optional[int] = Query(
            default=1,
            title='Номер страницы'
        )
) -> Pagination:
    return Pagination(size_page=size_page, number_page=number_page)


def create_meta(size_result: int, count: int, size_page: int, number_page: int) -> MetaPage:
    if size_page == -1:
        return MetaPage(
            count_objects=size_result,
            number_page=number_page,
            size_page=count,
            total_objects=count,
            total_pages=1
        )

    return MetaPage(
        count_objects=size_result,
        number_page=number_page,
        size_page=size_page,
        total_objects=count,
        total_pages=count // size_page + (count % size_page > 0)
    )
