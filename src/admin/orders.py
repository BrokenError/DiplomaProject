from sqladmin import ModelView

from db.models import Order


class OrderAdmin(ModelView, model=Order):
    column_list = '__all__'
    column_searchable_list = [Order.id]
    column_default_sort = [(Order.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Заказ"
    name_plural = "Заказы"
