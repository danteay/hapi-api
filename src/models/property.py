"""Property model definition."""

# pylint: disable=C0103

from pydbrepo import Entity, Field


class Property(Entity):
    """Property class model."""

    def __init__(self):
        self.id = Field(name='name', type_=int)
        self.address = Field(name='address', type_=str)
        self.city = Field(name='city', type_=str)
        self.price = Field(name='price', type_=int)
        self.description = Field(name='description', type_=str)
        self.year = Field(name='year', type_=str)
