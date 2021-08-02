"""Bad Request custom error."""

from typing import Any, List

from .handler_error import HandlerError


class BadRequestError(HandlerError):
    """Bad Request error class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=400,
            message='bad-request',
            description='Bad request',
            errors=errors,
            root_causes=root_causes,
        )
