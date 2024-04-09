from typing import Optional, Tuple, List

from sqlalchemy import func, select
from sqlalchemy.sql.selectable import Select

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import create_meta


class MixinPagination:

    async def list_paginated(self, query: Select, pagination: Pagination) -> dict:
        result, count = await self.get_page(query, pagination.size_page, pagination.number_page)
        return dict(
            items=result,
            meta=create_meta(
                len(result),
                count,
                pagination.size_page,
                pagination.number_page
            )
        )

    async def get_page(self, query: Select, size_page: int, number_page: int) -> Tuple[List, int]:
        if size_page == -1:
            return await self.get_fragment(query=query, limit=None, offset=0)

        return await self.get_fragment(query=query, limit=size_page, offset=(number_page - 1) * size_page)

    async def get_fragment(self, query: Select, limit: Optional[int], offset: int) -> Tuple[List, int]:
        query_count = select(func.count(1)).select_from(query)
        return (
            (await self.manager.execute(query.limit(limit).offset(offset))).scalars().all(),
            (await self.manager.execute(query_count)).scalar()
        )
