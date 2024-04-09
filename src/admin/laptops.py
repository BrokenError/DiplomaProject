from sqladmin import ModelView

from db.models import Laptop


class LaptopAdmin(ModelView, model=Laptop):
    column_list = '__all__'
    column_searchable_list = [Laptop.name, Laptop.id]
    column_default_sort = [(Laptop.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    category = "Категории товаров"
    plural = "Ноутбук"
    name_plural = "Ноутбуки"
