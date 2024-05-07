from admin.products import BaseTechnic
from db.models import Tablet
from field_names_ru import TabletFields


class TabletAdmin(BaseTechnic, model=Tablet):
    column_labels = TabletFields
    column_searchable_list = [Tablet.name, Tablet.id]
    column_default_sort = [(Tablet.id, True)]
    name = "Планшет"
    name_plural = "Планшеты"
