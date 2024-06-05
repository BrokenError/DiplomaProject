from sqladmin import ModelView

from db.models import Provider
from field_names_ru import ProviderFields


class ProviderAdmin(ModelView, model=Provider):
    column_list = '__all__'
    column_labels = ProviderFields
    form_excluded_columns = ['date_created']
    column_sortable_list = ['id', 'date_created']
    column_searchable_list = [Provider.label, Provider.contact_info, Provider.description, Provider.location]
    column_default_sort = [(Provider.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Поставщик"
    name_plural = "Поставщики"
