"""Custom types definition."""

# pylint: disable=C0103

from pydbrepo import EnumEntity


class PropertyStatus(EnumEntity):
    """Property status definition."""

    pre_venta = 3
    en_venta = 4
    vendido = 5
