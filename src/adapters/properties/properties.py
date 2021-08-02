"""Properties adapter methods."""

from typing import AnyStr, List, Optional

from pydbrepo.drivers.mysql import Mysql

from src.models import Property
from src.models.types import PropertyStatus
from src.ports.repositories import PropertiesRepository


def filter_properties(
    status: Optional[List[PropertyStatus]] = None,
    city: Optional[AnyStr] = None,
    year: Optional[int] = None
) -> Optional[List[Property]]:
    """Filter properties from user entries.

    :param status: Current property status
    :param year: Property year build
    :param city: Property city location
    :return Optional[List[Property]]: List of found properties
    """

    with Mysql() as driver:
        repo = PropertiesRepository(driver)
        properties = repo.find_by_filters(status, year, city)

    if not properties:
        return []

    return properties
