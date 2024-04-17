from sqladmin import ModelView

from db.models import Provider


class ProviderAdmin(ModelView, model=Provider):
    column_list = '__all__'
    column_searchable_list = [Provider.label, Provider.contact_info]
    column_default_sort = [(Provider.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Поставщик"
    name_plural = "Поставщики"
