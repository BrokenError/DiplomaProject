from typing import Any
from urllib.request import Request

from sqladmin import ModelView

from db.models import OrderItem
from field_names_ru import OrderItemFields


class OrderItemAdmin(ModelView, model=OrderItem):
    column_labels = OrderItemFields
    column_exclude_list = ['id_user', 'id_product', 'id_order']
    column_searchable_list = [OrderItem.id_product, OrderItem.id]
    column_default_sort = [(OrderItem.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Предметы заказа"
    name_plural = "Предметы заказов"

    async def insert_model(self, request: Request, data: dict) -> Any:
        if data['quantity'] < 0:
            raise ValueError('Количество должно быть больше нуля')
        return await super().insert_model(data=data, request=request)
