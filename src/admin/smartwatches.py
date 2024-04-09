from sqladmin import ModelView

from db.models import Smartwatch


class SmartwatchAdmin(ModelView, model=Smartwatch):
    column_list = '__all__'
    column_searchable_list = [Smartwatch.name, Smartwatch.id]
    column_default_sort = [(Smartwatch.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    category = "Категории товаров"
    plural = "Часы"
    name_plural = "Часы"
