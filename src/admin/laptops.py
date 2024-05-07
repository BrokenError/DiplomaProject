from admin.products import BaseTechnic
from db.models import Laptop
from field_names_ru import LaptopFields


class LaptopAdmin(BaseTechnic, model=Laptop):
    column_labels = LaptopFields
    column_searchable_list = [Laptop.name, Laptop.id]
    column_default_sort = [(Laptop.id, True)]
    name = "Ноутбук"
    name_plural = "Ноутбуки"
