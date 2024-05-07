from admin.products import BaseTechnic
from db.models import Television
from field_names_ru import TelevisionFields


class TelevisionAdmin(BaseTechnic, model=Television):
    column_labels = TelevisionFields
    column_searchable_list = [Television.name, Television.id]
    column_default_sort = [(Television.id, True)]
    name = "Телевизор"
    name_plural = "Телевизоры"
