from typing import Any

from apps.commons.basics.exceptions import ExceptionCRM


class ExceptionQuerystring(ExceptionCRM):
    def __init__(self, details: Any):
        super().__init__(
            code_status=400,
            details=details
        )
