from sqladmin import ModelView

from db.models import OrderItem


class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = '__all__'
    column_searchable_list = [OrderItem.id_product, OrderItem.id]
    column_default_sort = [(OrderItem.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Предметы заказа"
    name_plural = "Предметы заказов"
