"""Internal custom error."""

from typing import Any, List

from .handler_error import HandlerError


class InternalError(HandlerError):
    """Internal error class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=500,
            message='internal-error',
            description='Internal server error',
            errors=errors,
            root_causes=root_causes,
        )
