from sqladmin import ModelView

from db.models import Accessory


class AccessoryAdmin(ModelView, model=Accessory):
    column_list = '__all__'
    column_searchable_list = [Accessory.name, Accessory.id]
    column_default_sort = [(Accessory.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    category = "Категории товаров"
    plural = "Аксессуар"
    name_plural = "Аксессуары"
