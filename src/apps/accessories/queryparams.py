from typing import Optional

from fastapi import Query

from apps.commons.querystrings_v2.processor import queryparams


@queryparams
class FilterAccessory:
    color_main__in_arr: Optional[str] = Query(default=None, alias='color_main_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    brand__in_arr: Optional[str] = Query(default=None, alias='brand_in')
    model__in_arr: Optional[str] = Query(default=None, alias='model_in')
    material__in_arr: Optional[str] = Query(default=None, alias='material_in')
