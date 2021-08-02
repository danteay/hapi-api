"""Forbidden custom error."""

from typing import Any, List

from .handler_error import HandlerError


class ForbiddenError(HandlerError):
    """Forbidden error class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=403,
            message='forbidden',
            description='Forbidden resources access',
            errors=errors,
            root_causes=root_causes,
        )
