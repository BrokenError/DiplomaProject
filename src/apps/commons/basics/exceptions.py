from typing import Any


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
