from sqladmin import ModelView

from db.models import Favourite


class FavouriteAdmin(ModelView, model=Favourite):
    column_list = '__all__'
    column_searchable_list = [Favourite.id_product, Favourite.id_user]
    column_default_sort = [(Favourite.id_product, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Понравившийся товар"
    name_plural = "Понравившиеся товары"
