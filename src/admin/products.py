from typing import Any
from urllib.request import Request

from markupsafe import Markup
from sqladmin import ModelView

from apps.accessories.schemas import AccessoryAdminSchema
from apps.accessories.services import AccessoryService
from apps.commons.managers.base import ManagerBase
from apps.laptops.schemas import LaptopAdminSchema
from apps.products.schemas import ProductAdminSchema
from apps.smartphones.schemas import SmartphoneAdminSchema
from apps.smartwatches.schemas import SmartwatchAdminSchema
from apps.tablets.schemas import TabletAdminSchema
from apps.televisions.schemas import TelevisionAdminSchema
from db.database import SessionLocal
from db.models import Product, Photo, Accessory, Laptop, Tablet, Television, Smartphone, Smartwatch
from field_names_ru import PhotoFields, ProductFields
from settings import settings_app


class BaseTechnic(ModelView):
    column_list = [
        'id', 'photos', 'brand', 'model', 'type', 'price',
        'discount', 'quantity', 'color_main', 'is_active', 'is_deleted'
    ]
    form_excluded_columns = ['photos', 'is_deleted', 'date_created']
    category = "Категории товаров"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    def __init__(self):
        super().__init__()

    async def delete_model(self, request: Request, pk: Any) -> None:
        async with SessionLocal() as session:
            manager = ManagerBase(session=session)
            service = AccessoryService(manager=manager, id_user=False)
            await manager.update(
                await service.get_type_product(id_instance=int(pk)),
                {
                    'is_deleted': True
                }
            )

    @staticmethod
    def validate_data(data: dict, model) -> dict:
        schemas = {
            Product: ProductAdminSchema,
            Accessory: AccessoryAdminSchema,
            Laptop: LaptopAdminSchema,
            Tablet: TabletAdminSchema,
            Television: TelevisionAdminSchema,
            Smartphone: SmartphoneAdminSchema,
            Smartwatch: SmartwatchAdminSchema
        }

        data = schemas[model](**data, id_provider=data['provider'])
        return data.dict()

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        data = {**data, **self.validate_data(data, self.model)}
        if data['quantity'] < 1:
            data['is_active'] = False
        return await super().update_model(request, pk, data)

    async def insert_model(self, request: Request, data: dict) -> Any:
        data = {**data, **self.validate_data(data, self.model)}
        if data['quantity'] < 1:
            data['is_active'] = False
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
