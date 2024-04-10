from sqladmin import ModelView

from db.models import Product


class ProductAdmin(ModelView, model=Product):
    column_list = '__all__'
    column_searchable_list = [Product.name, Product.id]
    column_default_sort = [(Product.id, True)]
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True
    category = "Категории товаров"
    plural = "Товар"
    name_plural = "Товары"
