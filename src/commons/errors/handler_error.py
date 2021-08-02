"""Custom exceptions."""

from typing import Any, AnyStr, List


class HandlerError(Exception):
    """Main handler error."""

    def __init__(
        self,
        code: int,
        message: AnyStr,
        description: AnyStr,
        errors: Any = None,
        root_causes: List[Any] = None,
    ):
        super().__init__(message, errors)

        self.code = code
        self.message = message
        self.description = description
        self.errors = errors
        self.root_causes = root_causes
