"""Logging bootstrapping."""

import logging
import os

from elasticlogger import Logger

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
APP_NAME = os.getenv('APP_NAME', 'service')


def _get_logger_level() -> int:
    """Return the log level value to build logger instance.
    :return int: Logger level
    """

    if LOG_LEVEL == 'DEBUG':
        return logging.DEBUG

    if LOG_LEVEL == 'INFO':
        return logging.INFO

    if LOG_LEVEL == 'WARNING':
        return logging.WARNING

    if LOG_LEVEL == 'ERROR':
        return logging.ERROR

    return logging.INFO


LOGGER = Logger(APP_NAME, level=_get_logger_level())


def config_logs():
    """Bootstrap logger configuration options."""
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    LOGGER.logger.propagate = False
