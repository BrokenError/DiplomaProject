from sqladmin import ModelView

from db.models import User


class UserAdmin(ModelView, model=User):
    column_list = '__all__'
    column_searchable_list = [User.email, User.phone_number, User.first_name, User.last_name]
    column_default_sort = [(User.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Пользователь"
    name_plural = "Пользователи"
