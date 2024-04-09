from sqladmin import ModelView

from db.models import Tablet


class TabletAdmin(ModelView, model=Tablet):
    column_list = '__all__'
    column_searchable_list = [Tablet.name, Tablet.id]
    column_default_sort = [(Tablet.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    category = "Категории товаров"
    plural = "Планшет"
    name_plural = "Планшеты"

