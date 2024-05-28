from typing import Any
from urllib.request import Request

from markupsafe import Markup
from sqladmin import ModelView

from apps.accessories.services import AccessoryService
from apps.commons.managers.base import ManagerBase
from db.database import SessionLocal
from db.models import Product, Photo
from field_names_ru import PhotoFields, ProductFields
from settings import settings_app


class BaseTechnic(ModelView):
    column_exclude_list = ['id_author', 'id_product', 'id_provider', 'id_editor_last']
    form_excluded_columns = ['photos', 'is_deleted', 'date_created']
    category = "Категории товаров"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    async def delete_model(self, request: Request, pk: Any) -> None:
        async with SessionLocal() as session:
            manager = ManagerBase(session=session)
            service = AccessoryService(manager=manager, id_user=None)
            await manager.update(
                await service.get_type_product(int(pk)),
                {
                    'is_deleted': True
                }
            )

    @staticmethod
    def validate_data(data: dict):
        if data['type'] not in settings_app.CATEGORIES:
            raise ValueError(f"Неверный формат категории. Возможные значения: {', '.join(settings_app.CATEGORIES)}")
        elif min(data['height'], data['width'], data['weight'], data['thickness']) <= 0:
            raise ValueError('Размеры и вес товара должны быть больше нуля')
        elif min(data['price'], data['discount']) < 0:
            raise ValueError('Цена и скидка товара должна быть положительная')
        elif data['quantity'] < 0:
            raise ValueError('Количество товара должно быть положительное')
        return data

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        self.validate_data(data)
        return await super().update_model(request, pk, data)

    async def insert_model(self, request: Request, data: dict) -> Any:
        self.validate_data(data)
        return await super().insert_model(data=data, request=request)


def custom_photo_format(photo):
    if not photo:
        return ''
    formatted_photos = f'<img src="{settings_app.BASE_URL}{photo.url}" height=30px style="max-width: none">'
    return Markup(formatted_photos)


def format_photos(model, formatted_value):
    return [Markup(custom_photo_format(photo)) for photo in model.photos]


BaseTechnic.column_formatters = {
    'photos': format_photos
}
BaseTechnic.column_formatters_detail = {
    'photos': format_photos
}


class ProductAdmin(BaseTechnic, model=Product):
    column_labels = ProductFields
    column_searchable_list = [Product.name, Product.id]
    column_default_sort = [(Product.id, True)]
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True
    name = "Товар"
    name_plural = "Товары"


class PhotosAdmin(ModelView, model=Photo):
    column_list = '__all__'
    column_labels = PhotoFields
    column_searchable_list = [Photo.url, Photo.id]
    column_default_sort = [(Product.id, True)]
    column_formatters = {
        "url": lambda m, a: Markup(
            f'<img src="{settings_app.BASE_URL}{m.url}" height=40px alt="Фотография">'
        ) if m.url else ''
    }
    column_formatters_detail = {
        "url": lambda m, a: Markup(
            f'<a href="{settings_app.BASE_URL}{m.url}">{settings_app.BASE_URL}{m.url}</a>'
        ) if m.url else ''
    }
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "Фотография"
    name_plural = "Фотографии"
