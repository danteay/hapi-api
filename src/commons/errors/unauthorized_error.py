"""Unauthorized custom error."""

from typing import Any, List

from .handler_error import HandlerError


class UnauthorizedError(HandlerError):
    """Unauthorized error class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=401,
            message='unauthorized',
            description='Unauthorized resource access',
            errors=errors,
            root_causes=root_causes,
        )
