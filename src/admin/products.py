from sqladmin import ModelView

from db.models import Product, Photo


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


class PhotosAdmin(ModelView, model=Photo):
    column_list = '__all__'
    column_searchable_list = [Photo.url, Photo.id]
    column_default_sort = [(Product.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Фотография"
    name_plural = "Фотографии"
