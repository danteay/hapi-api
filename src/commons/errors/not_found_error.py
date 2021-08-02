"""Not Found custom error."""

from typing import Any, List

from .handler_error import HandlerError


class NotFoundError(HandlerError):
    """Internal error class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=404,
            message='not-found',
            description='Resource not found',
            errors=errors,
            root_causes=root_causes,
        )
