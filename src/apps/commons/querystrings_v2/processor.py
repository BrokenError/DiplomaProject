from dataclasses import asdict, dataclass
from typing import Callable, Generator, Tuple, Any, TYPE_CHECKING, Type, Union

from sqlalchemy import Column
from sqlalchemy.sql.elements import BinaryExpression

from apps.commons.querystrings_v2.exceptions import ExceptionQuerystring
from apps.commons.querystrings_v2.schemas import Direction

if TYPE_CHECKING:
    class QueryParams:

        def dict(self) -> dict:
            pass


def queryparams(
    cls=None, /,
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    match_args=True,
    kw_only=False,
    slots=False
) -> Type['QueryParams']:
    cls.dict = asdict
    return dataclass(# noqa
        cls,
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
        match_args=match_args,
        kw_only=kw_only,
        slots=slots
    )


class ProcessorOperations(type):

    def __new__(metacls, name, bases, namespace, **kwargs):
        if not bases:
            return super().__new__(metacls, name, bases, namespace, **kwargs)

        return super(ProcessorOperations, metacls).__new__(metacls, name, bases, {
            '_methods_allowed': dict(ProcessorOperations._get_operations(namespace))
        })

    @staticmethod
    def _get_operations(namespace):
        for name_field, value in namespace.items():
            if callable(value):
                yield value.__name__, value


class CQuery(metaclass=ProcessorOperations):

    _methods_allowed: dict[str, Callable[[Column, Any], BinaryExpression]]

    @classmethod
    def _get_field_and_method(cls, statement: str) -> Tuple[str, str]:
        candidates = list(name_method for name_method in cls._methods_allowed if statement.endswith(name_method))
        if candidates:
            name_method = max(candidates, key=len)
            field = statement.replace(name_method, '')
            if field:
                return field, name_method

        text_methods_allowed = ', '.join(cls._methods_allowed)
        raise ExceptionQuerystring(
            f"Unknown operation in filter: '{statement}'. Only these are allowed: {text_methods_allowed}"
        )

    @classmethod
    def parse_methods_filters(cls, filters: dict[str, Any]) -> Generator[Tuple[str, str, Any], None, None]:
        for statement, value in filters.items():
            field, name_method = cls._get_field_and_method(statement)
            if value is not None:
                yield field, name_method, value

    @staticmethod
    def get_ordering(ordering) -> Union[None, str]:
        if ordering.sort is None:
            return None
        field, direction = ordering.sort, ordering.sort.value
        if direction not in Direction:
            raise ExceptionQuerystring(f"Disallowed direction in sortings: '{field} - {direction}'.")
        return field

    def get_filters(self, model_db, dict_filters: dict[str, Any]) -> Generator[BinaryExpression, None, None]:
        errors = []
        for field, name_method, value in self.parse_methods_filters(dict_filters):
            method = self._methods_allowed.get(name_method)

            if method is None:
                errors.append(f"Unknown method '{name_method}' for field '{field}'.")

            if not errors:
                field = getattr(model_db, field)
                yield method(field, value)

        if errors:
            raise ExceptionQuerystring(errors)
