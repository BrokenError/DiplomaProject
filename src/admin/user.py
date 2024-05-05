import re
from typing import Any

import wtforms
from sqladmin import ModelView
from starlette.requests import Request

from apps.commons.managers.base import ManagerBase
from db.database import SessionLocal
from db.models import User, Order
from field_names_ru import UserFields
from settings import settings_app


class UserAdmin(ModelView, model=User):
    column_list = '__all__'
    column_labels = UserFields
    form_excluded_columns = ['date_created']
    column_searchable_list = [User.email, User.phone_number, User.first_name, User.last_name]
    column_default_sort = [(User.id, True)]
    can_create = True
    form_overrides = dict(email=wtforms.EmailField)
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Пользователь"
    name_plural = "Пользователи"

    async def insert_model(self, request: Request, data: dict) -> Any:
        if not re.match(settings_app.EMAIL_REGEX, data['email']):
            raise ValueError('Неверный формат почты')

        user = await super().insert_model(data=data, request=request)

        async with SessionLocal() as session:
            manager = ManagerBase(session=session)
            order = await manager.create(
                Order,
                {"description": "Корзина пользователя", "status": "cart"} | {"id_user": int(user.id)}
            )
            await manager.session.refresh(order)
        return user
