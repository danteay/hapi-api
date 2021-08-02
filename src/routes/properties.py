"""Ping lambda methods."""

from typing import Any, AnyStr, Dict

from src.commons import http
from src.commons.logging import config_logs
from src.commons.middlewares import request
from src.handlers import properties

config_logs()


@request.validate()
def find(*_) -> Dict[AnyStr, Any]:
    """Filter properties."""

    try:
        return http.json(body=properties.find())
    except Exception as error:
        return http.json_error(error)
