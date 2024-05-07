import logging
from typing import Optional

from fastapi import HTTPException

from apps.commons.services import ServiceBase
# from apps.reviews.schemas import ReviewIn
from db.models import Review

logger = logging.getLogger('smartphones')


class ReviewService(ServiceBase):
    Model = Review

    async def create(self, *, data=None, data_extra: Optional[dict] = None) -> Model:
        data = dict(data) | {"id_user": self.id_user} | data_extra
        if await self.check_exists(id_user=data['id_user'], id_product=data_extra['id_product']):
            raise HTTPException(status_code=409, detail="Отзыв уже написан")
        review = await self.manager.create(self.Model, data)
        return review
