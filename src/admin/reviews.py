from http.client import HTTPException
from typing import Any
from urllib.request import Request

from sqladmin import ModelView

from apps.commons.managers.base import ManagerBase
from apps.reviews.services import ReviewService
from db.database import SessionLocal
from db.models import Review
from field_names_ru import ReviewFields


class ReviewAdmin(ModelView, model=Review):
    column_labels = ReviewFields
    column_exclude_list = ['id_user', 'id_product']
    form_excluded_columns = ['date_created']
    column_searchable_list = [Review.text, Review.id_product, Review.id_user]
    column_default_sort = [(Review.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Отзыв"
    name_plural = "Отзывы"

    @staticmethod
    def validate_data(data):
        if not 0 < data['rating'] < 6:
            raise ValueError('Оценка должна быть от 1 до 5')

    async def insert_model(self, request: Request, data: dict) -> Any:
        self.validate_data(data)
        id_user = int(data['user'])
        async with SessionLocal() as session:
            service = ReviewService(manager=ManagerBase(session=session), id_user=id_user)
            if await service.check_exists(id_user=id_user, id_product=int(data['product'])):
                raise ValueError('Отзыв уже существует')
        return await super().insert_model(data=data, request=request)

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        self.validate_data(data)
        return await super().update_model(request=request, pk=pk, data=data)
