from contextlib import contextmanager
from typing import Any

from fastapi import HTTPException
from pydantic_core import ValidationError


class ExceptionCRM(Exception):
    def __init__(self, code_status: int, details: Any):
        self.code_status = code_status
        self.details = details


class ExceptionValidation(ExceptionCRM):
    def __init__(self, details: Any):
        super().__init__(
            code_status=400,
            details=details
        )


class CustomValidationException(HTTPException):
    def __init__(self, detail: str):
        self.field = None
        super().__init__(status_code=422, detail=detail)


@contextmanager
def validation_context(detail: str, field: Any = None):
    try:
        yield
    except (ValueError, ValidationError):
        detail = f'Неверное значение поля «{field}». {detail}'
        raise CustomValidationException(detail)


class ExceptionNotFound(ExceptionCRM):
    def __init__(self, details: Any):
        super().__init__(
            code_status=404,
            details=details
        )


class ExceptionForbidden(ExceptionCRM):
    def __init__(self, details: Any):
        super().__init__(
            code_status=403,
            details=details
        )
