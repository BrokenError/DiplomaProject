from sqladmin import ModelView

from db.models import Television


class TelevisionAdmin(ModelView, model=Television):
    column_list = '__all__'
    column_searchable_list = [Television.name, Television.id]
    column_default_sort = [(Television.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    category = "Категории товаров"
    plural = "Телевизор"
    name_plural = "Телевизоры"
