from admin.products import BaseTechnic

from db.models import Accessory
from field_names_ru import AccessoryFields


class AccessoryAdmin(BaseTechnic, model=Accessory):
    column_labels = AccessoryFields
    column_searchable_list = [Accessory.name, Accessory.id]
    column_default_sort = [(Accessory.id, True)]
    name = "Аксессуар"
    name_plural = "Аксессуары"
