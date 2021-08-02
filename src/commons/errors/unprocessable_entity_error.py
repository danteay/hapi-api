"""Unprocessable Entity custom error."""

from typing import Any, List

from .handler_error import HandlerError


class UnprocessableEntityError(HandlerError):
    """Unprocessable Entity class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=422,
            message='unprocessable-entity',
            description='Unprocessable resource entity',
            errors=errors,
            root_causes=root_causes,
        )
