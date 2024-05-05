from admin.products import BaseTechnic
from db.models import Smartwatch
from field_names_ru import SmartwatchFields


class SmartwatchAdmin(BaseTechnic, model=Smartwatch):
    column_labels = SmartwatchFields
    column_searchable_list = [Smartwatch.name, Smartwatch.id]
    column_default_sort = [(Smartwatch.id, True)]
    name = "Часы"
    name_plural = "Часы"
