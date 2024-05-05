from sqladmin import ModelView

from db.models import Favourite
from field_names_ru import FavouriteFields


class FavouriteAdmin(ModelView, model=Favourite):
    column_labels = FavouriteFields
    column_exclude_list = ['id_user', 'id_product']
    form_excluded_columns = ['is_deleted']
    column_searchable_list = [Favourite.id_product, Favourite.id_user]
    column_default_sort = [(Favourite.id_product, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Понравившийся товар"
    name_plural = "Понравившиеся товары"
