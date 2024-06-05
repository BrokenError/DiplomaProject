from typing import Optional

from fastapi import Query

from apps.commons.querystrings_v2.processor import queryparams


@queryparams
class FilterSmartwatch:
    color_main__in_arr: Optional[str] = Query(default=None, alias='color_main_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    brand__in_arr: Optional[str] = Query(default=None, alias='brand_in')
    model__in_arr: Optional[str] = Query(default=None, alias='model_in')
    material__in_arr: Optional[str] = Query(default=None, alias='material_in')
    date_release__yyyy_in: Optional[str] = Query(default=None, alias='date_release_in')
    screen_diagonal__in_arr: Optional[str] = Query(default=None, alias='screen_diagonal_in')
    degree_protection__in_arr: Optional[str] = Query(default=None, alias='degree_protection_in')
    water_resistance__in_arr: Optional[str] = Query(default=None, alias='water_resistance_in')
