"""Properties handler methods."""

from typing import Any, AnyStr, Dict

from src.adapters import properties
from src.commons import context
from src.helpers import properties as helpers


def find() -> Dict[AnyStr, Any]:
    """Filter properties."""

    query_params = context.get_value('request').get('query_params', {})
    status_ids = query_params.get('status', None)
    city = query_params.get('city', None)
    year = query_params.get('year', None)

    if year is not None:
        year = int(year)

    status_ids = helpers.transform_status_from_params(status_ids)
    filtered_properties = properties.filter_properties(status_ids, city, year)

    return {'properties': [item.to_dict() for item in filtered_properties]}
