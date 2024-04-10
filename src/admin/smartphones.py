from sqladmin import ModelView

from db.models import Smartphone


class SmartphoneAdmin(ModelView, model=Smartphone):
    column_list = '__all__'
    column_searchable_list = [Smartphone.name, Smartphone.id]
    column_default_sort = [(Smartphone.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    category = "Категории товаров"
    plural = "Телефон"
    name_plural = "Телефоны"
