import json

from sqlalchemy import not_, and_, or_, func

from apps.commons.querystrings_v2.processor import CQuery
from db.models import Product


class QueryFilter(CQuery):

    @staticmethod
    def __eq(field, value):
        return field == value

    @staticmethod
    def __not_eq(field, value):
        return field != value

    @staticmethod
    def __matches(field, value):
        return field.like(value)

    @staticmethod
    def __does_not_match(field, value):
        return not_(field.like(value))

    @staticmethod
    def __matches_any(field, values):
        return or_(*[field.like(val) for val in values])

    @staticmethod
    def __matches_any_arr(field, value):
        return or_(*[field.like(val) for val in json.loads(value)])

    @staticmethod
    def __matches_all(field, values):
        return and_(*[field.like(val) for val in values])

    @staticmethod
    def __matches_all_arr(field, value):
        return and_(*[field.like(val) for val in json.loads(value)])

    @staticmethod
    def __does_not_match_any(field, values):
        return or_(*[field.like(val) for val in values])

    @staticmethod
    def __does_not_match_any_arr(field, value):
        return or_(*[field.like(val) for val in json.loads(value)])

    @staticmethod
    def __does_not_match_all(field, value):
        return and_(*[not_(field.like(sub_val)) for sub_val in value])

    @staticmethod
    def __lt(field, value):
        return field < value

    @staticmethod
    def __lte(field, value):
        return or_(
            and_(Product.discount > 0, field * (1 - Product.discount / 100.0) - 1 <= value),
            and_(Product.discount == 0, field <= value)
        )

    @staticmethod
    def __gt(field, value):
        return field > value

    @staticmethod
    def __gte(field, value):
        return or_(
            and_(Product.discount > 0, field * (1 - Product.discount / 100.0) + 1 >= value),
            and_(Product.discount == 0, field >= value)
        )

    @staticmethod
    def __present(field, value):
        return and_(field != None, field != '')  # noqa

    @staticmethod
    def __blank(field, value):
        return or_(field == None, field == '')  # noqa

    @staticmethod
    def __null(field, value):
        return field.is_(None)

    @staticmethod
    def __not_null(field, value):
        return field.is_not(None)

    @staticmethod
    def __in(field, values):
        return field.in_(values)

    @staticmethod
    def __in_arr(field, value):
        return field.in_(json.loads(value))

    @staticmethod
    def __not_in(field, values):
        return not_(field.in_(values))

    @staticmethod
    def __not_in_arr(field, value):
        return not_(field.in_(json.loads(value)))

    @staticmethod
    def __lt_any(field, values):
        return or_(*[field < val for val in values])

    @staticmethod
    def __lt_any_arr(field, value):
        return or_(*[field < val for val in json.loads(value)])

    @staticmethod
    def __lte_any(field, values):
        return or_(*[field <= val for val in values])

    @staticmethod
    def __lte_any_arr(field, value):
        return or_(*[field <= val for val in json.loads(value)])

    @staticmethod
    def __gt_any(field, values):
        return or_(*[field > val for val in values])

    @staticmethod
    def __gt_any_arr(field, value):
        return or_(*[field > val for val in json.loads(value)])

    @staticmethod
    def __gte_any(field, values):
        return or_(*[field >= val for val in values])

    @staticmethod
    def __gte_any_arr(field, value):
        return or_(*[field >= val for val in json.loads(value)])

    @staticmethod
    def __lt_all(field, values):
        return and_(*[field < val for val in values])

    @staticmethod
    def __lt_all_arr(field, value):
        return and_(*[field < val for val in json.loads(value)])

    @staticmethod
    def __lte_all(field, values):
        return and_(*[field <= val for val in values])

    @staticmethod
    def __lte_all_arr(field, value):
        return and_(*[field <= val for val in json.loads(value)])

    @staticmethod
    def __gt_all(field, values):
        return and_(*[field > val for val in values])

    @staticmethod
    def __gt_all_arr(field, value):
        return and_(*[field > val for val in json.loads(value)])

    @staticmethod
    def __gte_all(field, values):
        return and_(*[field >= val for val in values])

    @staticmethod
    def __gte_all_arr(field, value):
        return and_(*[field >= val for val in json.loads(value)])

    @staticmethod
    def __not_eq_all(field, values):
        return and_(*[field != val for val in values])

    @staticmethod
    def __not_eq_all_arr(field, value):
        return and_(*[field != val for val in json.loads(value)])

    @staticmethod
    def __start(field, value):
        return field.like(f'{value}%')

    @staticmethod
    def __not_start(field, value):
        return not_(field.like(f'{value}%'))

    @staticmethod
    def __start_any(field, values):
        return or_(*[field.like(f'{val}%') for val in values])

    @staticmethod
    def __start_any_arr(field, value):
        return or_(*[field.like(f'{val}%') for val in json.loads(value)])

    @staticmethod
    def __not_start_any(field, values):
        return or_(*[not_(field.like(f'{val}%')) for val in values])

    @staticmethod
    def __not_start_any_arr(field, value):
        return or_(*[not_(field.like(f'{val}%')) for val in json.loads(value)])

    @staticmethod
    def __not_start_all(field, values):
        return and_(*[not_(field.like(f'{val}%')) for val in values])

    @staticmethod
    def __not_start_all_arr(field, value):
        return and_(*[not_(field.like(f'{val}%')) for val in json.loads(value)])

    @staticmethod
    def __end(field, value):
        return field.like(f'%{value}')

    @staticmethod
    def __not_end(field, value):
        return not_(field.like(f'%{value}'))

    @staticmethod
    def __end_any(field, values):
        return or_(*[not_(field.like(f'%{val}')) for val in values])

    @staticmethod
    def __end_any_arr(field, value):
        return or_(*[not_(field.like(f'%{val}')) for val in json.loads(value)])

    # @staticmethod
    # def __end_all(field, value):  # ????
    #     return

    @staticmethod
    def __not_end_any(field, values):
        return and_(*[not_(field.like(f'%{val}')) for val in values])

    @staticmethod
    def __not_end_any_arr(field, value):
        return and_(*[not_(field.like(f'%{val}')) for val in json.loads(value)])

    # @staticmethod
    # def __not_end_all(field, value):
    #     pass

    @staticmethod
    def __cont(field, value):
        return field.contains(value)

    @staticmethod
    def __cont_any(field, values):
        return or_(*[field.contains(val) for val in values])

    @staticmethod
    def __cont_any_arr(field, value):
        return or_(*[field.contains(val) for val in value])

    @staticmethod
    def __cont_all(field, values):
        return and_(*[field.contains(val) for val in values])

    @staticmethod
    def __cont_all_arr(field, value):
        return and_(*[field.contains(val) for val in json.loads(value)])

    @staticmethod
    def __not_cont(field, value):
        return not_(field.contains(value))

    @staticmethod
    def __not_cont_any(field, values):
        return or_(*[not_(field.contains(val)) for val in values])

    @staticmethod
    def __not_cont_any_arr(field, value):
        return or_(*[not_(field.contains(val)) for val in json.loads(value)])

    @staticmethod
    def __not_cont_all(field, values):
        return and_(*[not_(field.contains(val)) for val in values])

    @staticmethod
    def __not_cont_all_arr(field, value):
        return and_(*[not_(field.contains(val)) for val in json.loads(value)])

    @staticmethod
    def __i_cont(field, value):
        return func.lower(field).contains(value.lower())

    @staticmethod
    def __i_cont_any(field, values):
        return or_(*[func.lower(field).contains(val.lower()) for val in values])

    @staticmethod
    def __i_cont_any_arr(field, value):
        return or_(*[func.lower(field).contains(val.lower()) for val in json.loads(value)])

    @staticmethod
    def __i_cont_all(field, values):
        return and_(*[func.lower(field).contains(val.lower()) for val in values])

    @staticmethod
    def __i_cont_all_arr(field, value):
        return and_(*[func.lower(field).contains(val.lower()) for val in json.loads(value)])

    @staticmethod
    def __not_i_cont(field, value):
        return not_(func.lower(field).contains(value.lower()))

    @staticmethod
    def __not_i_cont_any(field, values):
        return or_(*[func.lower(field).contains(val.lower()) for val in values])

    @staticmethod
    def __not_i_cont_any_arr(field, value):
        return or_(*[func.lower(field).contains(val.lower()) for val in json.loads(value)])

    @staticmethod
    def __not_i_cont_all(field, values):
        return and_(*[func.lower(field).contains(val.lower()) for val in values])

    @staticmethod
    def __not_i_cont_all_arr(field, value):
        return and_(*[func.lower(field).contains(val.lower()) for val in json.loads(value)])

    @staticmethod
    def __true(field, value):
        return field == True  # noqa

    @staticmethod
    def __false(field, value):
        return field == False  # noqa

    @staticmethod
    def __dd_eq(field, value):
        return func.extract('day', field) == value

    @staticmethod
    def __mm_eq(field, value):
        return func.extract('month', field) == value

    @staticmethod
    def __yyyy_eq(field, value):
        return func.extract('year', field) == value

    @staticmethod
    def __yyyy_in(field, values):
        return or_(*[func.extract('year', field) == year for year in json.loads(values)])

    @staticmethod
    def __dd_lt(field, value):
        return func.extract('day', field) < value

    @staticmethod
    def __mm_lt(field, value):
        return func.extract('month', field) < value

    @staticmethod
    def __yyyy_lt(field, value):
        return func.extract('year', field) < value

    @staticmethod
    def __dd_lte(field, value):
        return func.extract('day', field) <= value

    @staticmethod
    def __mm_lte(field, value):
        return func.extract('month', field) <= value

    @staticmethod
    def __yyyy_lte(field, value):
        return func.extract('year', field) <= value

    @staticmethod
    def __dd_gt(field, value):
        return func.extract('day', field) > value

    @staticmethod
    def __mm_gt(field, value):
        return func.extract('month', field) > value

    @staticmethod
    def __yyyy_gt(field, value):
        return func.extract('year', field) > value

    @staticmethod
    def __dd_gte(field, value):
        return func.extract('day', field) >= value

    @staticmethod
    def __mm_gte(field, value):
        return func.extract('month', field) >= value

    @staticmethod
    def __yyyy_gte(field, value):
        return func.extract('year', field) >= value
