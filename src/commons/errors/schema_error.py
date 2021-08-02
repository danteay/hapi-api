"""Custom schema error."""

from typing import Any

from .handler_error import HandlerError


class SchemaError(HandlerError):
    """JSON Schema validation error."""

    def __init__(self, errors: Any):
        super().__init__(
            code=400,
            message='bad-request',
            description='Schema validation error',
            errors=errors,
            root_causes=[{
                'error': errors.args[0].split(':  ')[0],
            }],
        )
