import enum
from enum import Enum


class EnumMetaCheckable(enum.EnumMeta):
    def __contains__(cls, item):
        return item in cls.__members__.values()


class Direction(str, Enum, metaclass=EnumMetaCheckable):
    popular = 'popular'
    price_asc = 'price_asc'
    price_desc = 'price_desc'
    discount_desc = 'discount_desc'
    rating_desc = 'rating_desc'
