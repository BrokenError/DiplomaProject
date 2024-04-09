from sqladmin import ModelView

from db.models import LikedProduct


class LikedProductAdmin(ModelView, model=LikedProduct):
    column_list = '__all__'
    column_searchable_list = [LikedProduct.id_product, LikedProduct.id_user]
    column_default_sort = [(LikedProduct.id_product, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Понравившийся товар"
    name_plural = "Понравившиеся товары"
