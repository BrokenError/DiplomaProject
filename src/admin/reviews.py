from sqladmin import ModelView

from db.models import Review


class ReviewAdmin(ModelView, model=Review):
    column_list = '__all__'
    column_searchable_list = [Review.text, Review.id_product, Review.id_user]
    column_default_sort = [(Review.id, True)]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    plural = "Отзыв"
    name_plural = "Отзывы"
