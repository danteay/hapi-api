"""Data Conflict custom error."""

from typing import Any, List

from .handler_error import HandlerError


class DataConflictError(HandlerError):
    """Data Conflict error class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=409,
            message='data-conflict',
            description='Resource data conflict',
            errors=errors,
            root_causes=root_causes,
        )
