from typing import Optional, List

from fastapi import Query

from apps.commons.querystrings_v2.processor import queryparams
from apps.commons.querystrings_v2.schemas import Direction


@queryparams
class OrderingProduct:
    sort: Optional[Direction] = (Query(default=None))


@queryparams
class FilterProduct:
    color_main__in_arr: Optional[List[str]] = Query(default=None, alias='color_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    model__in_arr: Optional[List[str]] = Query(default=None, alias='model_in')
    material__in_arr: Optional[List[str]] = Query(default=None, alias='material_in')


@queryparams
class FilterSmartphone:
    color_main__in_arr: Optional[List[str]] = Query(default=None, alias='color_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    model__in_arr: Optional[List[str]] = Query(default=None, alias='model_in')
    material__in_arr: Optional[List[str]] = Query(default=None, alias='material_in')
    memory__in_arr: Optional[List[int]] = Query(default=None, alias='memory_in')
    memory_ram__in_arr: Optional[List[str]] = Query(default=None, alias='memory_ram_in')
    date_release__yyyy_eq: Optional[List[str]] = Query(default=None, alias='date_release_in')
    accumulator_capacity__in_arr: Optional[List[int]] = Query(default=None, alias='accumulator_capacity_in')
    matrix_frequency__in_arr: Optional[List[int]] = Query(default=None, alias='matrix_frequency_in')
    screen_diagonal__in_arr: Optional[List[str]] = Query(default=None, alias='screen_diagonal_in')
    number_cores__in_arr: Optional[List[int]] = Query(default=None, alias='number_cores_in')


@queryparams
class FilterLaptop:
    color_main__in_arr: Optional[List[str]] = Query(default=None, alias='color_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    model__in_arr: Optional[List[str]] = Query(default=None, alias='model_in')
    material__in_arr: Optional[List[str]] = Query(default=None, alias='material_in')
    memory_ram__in_arr: Optional[List[str]] = Query(default=None, alias='memory_ram_in')
    screen_diagonal__in_arr: Optional[List[str]] = Query(default=None, alias='screen_diagonal_in')
    processor_model__in_arr: Optional[List[str]] = Query(default=None, alias='processor_model_in')
    video_card_model__in_arr: Optional[List[str]] = Query(default=None, alias='video_card_model_in')
    matrix_type__in_arr: Optional[List[str]] = Query(default=None, alias='matrix_type_in')
    number_cores__in_arr: Optional[List[int]] = Query(default=None, alias='number_cores_in')


@queryparams
class FilterAccessory:
    color_main__in_arr: Optional[List[str]] = Query(default=None, alias='color_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    model__in_arr: Optional[List[str]] = Query(default=None, alias='model_in')
    material__in_arr: Optional[List[str]] = Query(default=None, alias='material_in')


@queryparams
class FilterTelevision:
    color_main__in_arr: Optional[List[str]] = Query(default=None, alias='color_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    model__in_arr: Optional[List[str]] = Query(default=None, alias='model_in')
    material__in_arr: Optional[List[str]] = Query(default=None, alias='material_in')
    screen_diagonal__in_arr: Optional[List[str]] = Query(default=None, alias='screen_diagonal_in')
    screen_resolution__in_arr: Optional[List[str]] = Query(default=None, alias='screen_resolution_in')
    matrix_frequency__in_arr: Optional[List[str]] = Query(default=None, alias='matrix_frequency_in')


@queryparams
class FilterSmartwatch:
    color_main__in_arr: Optional[List[str]] = Query(default=None, alias='color_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    model__in_arr: Optional[List[str]] = Query(default=None, alias='model_in')
    material__in_arr: Optional[List[str]] = Query(default=None, alias='material_in')
    screen_diagonal__in_arr: Optional[List[str]] = Query(default=None, alias='screen_diagonal_in')
    degree_protection__in_arr: Optional[List[str]] = Query(default=None, alias='degree_protection_in')
    water_resistance__in_arr: Optional[List[str]] = Query(default=None, alias='water_resistance_in')


@queryparams
class FilterTablet:
    color_main__in_arr: Optional[List[str]] = Query(default=None, alias='color_in')
    price__gte: Optional[int] = Query(default=None, alias='price_gte')
    price__lte: Optional[int] = Query(default=None, alias='price_lte')
    model__in_arr: Optional[List[str]] = Query(default=None, alias='model_in')
    material__in_arr: Optional[List[str]] = Query(default=None, alias='material_in')
    memory__in_arr: Optional[List[int]] = Query(default=None, alias='memory_in')
    memory_ram__in_arr: Optional[List[str]] = Query(default=None, alias='memory_ram_in')
    date_release__yyyy_eq: Optional[List[str]] = Query(default=None, alias='date_release_in')
    accumulator_capacity__in_arr: Optional[List[int]] = Query(default=None, alias='accumulator_capacity_in')
    matrix_frequency__in_arr: Optional[List[int]] = Query(default=None, alias='matrix_frequency_in')
    screen_diagonal__in_arr: Optional[List[str]] = Query(default=None, alias='screen_diagonal_in')
    number_cores__in_arr: Optional[List[int]] = Query(default=None, alias='number_cores_in')
