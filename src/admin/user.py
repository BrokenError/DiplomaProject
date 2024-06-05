from typing import Any

import wtforms
from markupsafe import Markup
from sqladmin import ModelView
from starlette.requests import Request

from apps.commons.managers.base import ManagerBase
from apps.orders.schemas import OrderStatus
from apps.users.schemas import UserAdminSchema
from db.database import SessionLocal
from db.models import User, Order
from field_names_ru import UserFields
from settings import settings_app


class UserAdmin(ModelView, model=User):
    column_list = '__all__'
    column_labels = UserFields
    column_sortable_list = ['id', 'date_created']
    column_formatters = {
        "photo_url": lambda m, a: Markup(
            f'<a href="{settings_app.BASE_URL}{m.photo_url}">{settings_app.BASE_URL}{m.photo_url}</a>'
        ) if m.photo_url else ''
    }
    column_formatters_detail = {
        "photo_url": lambda m, a: Markup(
            f'<a href="{settings_app.BASE_URL}{m.photo_url}">{settings_app.BASE_URL}{m.photo_url}</a>'
        ) if m.photo_url else ''
    }
    form_excluded_columns = ['date_created']
    column_searchable_list = [User.email, User.phone_number, User.first_name, User.last_name]
    column_default_sort = [(User.id, True)]
    can_create = True
    form_overrides = dict(email=wtforms.EmailField)
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True
    plural = "Пользователь"
    name_plural = "Пользователи"

    async def insert_model(self, request: Request, data: dict) -> Any:
        data = UserAdminSchema(**data).dict()

        user = await super().insert_model(data=data, request=request)

        async with SessionLocal() as session:
            manager = ManagerBase(session=session)
            order = await manager.create(
                Order,
                {"status": OrderStatus.cart, "payment_method": "Отсутствует"} | {"id_user": int(user.id)}
            )
            await manager.session.refresh(order)
        return user
