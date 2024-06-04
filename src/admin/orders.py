from typing import Any
from urllib.request import Request

from sqladmin import ModelView

from apps.orders.schemas import OrderAdminSchema
from db.models import Order
from field_names_ru import OrderFields


class OrderAdmin(ModelView, model=Order):
    column_labels = OrderFields
    column_exclude_list = ['id_user', 'order_items']
    form_excluded_columns = ['is_deleted', 'order_items', 'date_created']
    column_searchable_list = [Order.id]
    column_default_sort = [(Order.id, True)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    name = "Заказ"
    name_plural = "Заказы"

    async def insert_model(self, request: Request, data: dict) -> Any:
        data = OrderAdminSchema(**data).dict()
        return await super().insert_model(data=data, request=request)
