"""Properties helper functions."""

from typing import AnyStr, List, Optional

from src.commons.logging import logger
from src.models.types import PropertyStatus


def transform_status_from_params(statuses: Optional[AnyStr] = None) -> Optional[List[PropertyStatus]]:
    """Transform and cast status from query params to valid PropertyStatus codes.

    :param statuses: Value of the status query param (comma separated string)
    :return Optional[List[PropertyStatus]]: List of casted statuses
    """

    if statuses is None:
        return None

    aux = []

    for status in statuses.split(','):
        try:
            aux.append(PropertyStatus(int(status)))
        except Exception as err:
            logger.field('status', status).err(err).warning('skipping wrong property status')

    if not aux:
        return None

    return aux
