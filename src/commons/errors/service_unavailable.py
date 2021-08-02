"""Internal custom error."""

from typing import Any, List

from .handler_error import HandlerError


class ServiceUnavailableError(HandlerError):
    """Service unavailable error class."""

    def __init__(self, errors: Any = None, root_causes: List[Any] = None):
        super().__init__(
            code=503,
            message='service-unavailable',
            description='Service is currently in maintenance mode',
            errors=errors,
            root_causes=root_causes,
        )
