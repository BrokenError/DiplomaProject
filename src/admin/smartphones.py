from admin.products import BaseTechnic
from db.models import Smartphone
from field_names_ru import SmartphoneFields


class SmartphoneAdmin(BaseTechnic, model=Smartphone):
    column_labels = SmartphoneFields
    column_searchable_list = [Smartphone.name, Smartphone.id]
    column_default_sort = [(Smartphone.id, True)]
    name = "Телефон"
    name_plural = "Телефоны"
