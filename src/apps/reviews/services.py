import logging
from typing import Optional

from fastapi import HTTPException

from apps.commons.services import ServiceBase
from apps.products.services import ProductService
from apps.reviews.schemas import ReviewIn, ReviewUpdate
from db.models import Review

logger = logging.getLogger('reviews')


class ReviewService(ServiceBase):
    Model = Review

    async def create(
            self,
            *,
            data=ReviewIn,
            data_extra: Optional[dict] = None,
            product_service: ProductService = None) -> Model:
        data = (
            await self.validate_data(None, data)
        ).dict(exclude_unset=True, exclude_none=True) if data else dict()
        if await self.check_exists(id_user=self.id_user, id_product=data_extra['id_product']):
            raise HTTPException(status_code=409, detail="Отзыв уже написан")
        if not await product_service.check_exists(id=data_extra['id_product']):
            raise HTTPException(status_code=404, detail="Товара не существует")
        review = await self.manager.create(self.Model, data | data_extra | {"id_user": self.id_user})
        return review

    async def get_instance_by_id_product(self, id_product: int) -> Model:
        instance = (await self.manager.execute(self.select_visible(id_product=id_product, id_user=self.id_user))).scalars().first()
        if instance:
            return instance.id

    async def update(
            self,
            id_instance: Optional[int] = None,
            *,
            data: Optional[ReviewUpdate] = None,
            data_extra: Optional[dict] = None
    ) -> Model:
        return await super().update(id_instance, data=data, data_extra={"id_user": self.id_user})
