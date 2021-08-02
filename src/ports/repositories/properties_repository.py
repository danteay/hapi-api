"""Properties repository implementation."""

# pylint: disable=E1101

from typing import Any, AnyStr, List, Optional, Tuple

from pydbrepo.drivers.mysql import Mysql
from pydbrepo.repository.mysql_repository import MysqlRepository
from pypika import Field
from pypika import MySQLQuery as Query
from pypika import Parameter

from src.models import Property
from src.models.types import PropertyStatus


class PropertiesRepository(MysqlRepository):
    """Properties class repository."""

    def __init__(self, driver: Mysql):
        super().__init__(driver=driver, table='property', entity=Property)

    def find_by_filters(
        self,
        statuses: Optional[List[PropertyStatus]] = None,
        year: Optional[int] = None,
        city: Optional[AnyStr] = None,
    ) -> Optional[List[Property]]:
        """Find all available properties by the given filters.

        :param statuses: Current property status
        :param year: Property year build
        :param city: Property city location
        :return Optional[List[Property]]: List of found properties
        """

        values = self._get_property_ids_by_status(statuses)

        if values is None:
            return None

        args = [Parameter(self.driver.placeholder()) for _ in range(len(values))]

        sql_query = Query.from_(self._table).select(*self.entity_properties)
        sql_query = sql_query.where(Field('id').isin(args))

        if year is not None:
            values.append(year)
            sql_query = sql_query.where(Field('year') == Parameter(self.driver.placeholder()))

        if city is not None:
            values.append(city)
            sql_query = sql_query.where(Field('city') == Parameter(self.driver.placeholder()))

        records = self.driver.query(sql=str(sql_query), args=values)

        if not records:
            return None

        return [self.entity.from_record(self.entity_properties, record) for record in records]

    @staticmethod
    def _build_status_filter(status: Optional[List[PropertyStatus]] = None) -> Tuple[List[Any], List[AnyStr]]:
        """Validate status that will be used as filters on find_by_filters method and return
        a tuple with the list of values an a list with the corresponding SQL placeholders.

        :param status: Current property status
        :return Tuple[List[PropertyStatus], List[AnyStr]]: (statuses, status_place_holders)
        """

        status_place_holders = ['%s', '%s', '%s']
        values = [
            PropertyStatus.pre_venta.value,
            PropertyStatus.en_venta.value,
            PropertyStatus.vendido.value,
        ]

        if status is not None:
            values = [item.value for item in status]
            status_place_holders = ['%s' for _ in range(len(values))]

        return values, status_place_holders

    def _get_property_ids_by_status(self, statuses: Optional[List[PropertyStatus]] = None) -> Optional[List[int]]:
        """List of property ids by his last status"""

        values, place_holders = self._build_status_filter(statuses)
        place_holders = ",".join(place_holders)

        sql = (
            "SELECT property_id from ("
            "SELECT sh.property_id AS property_id, sh.status_id AS status_id "
            "FROM status_history sh "
            "WHERE status_id IN (3, 4, 5) "
            "GROUP BY sh.property_id "
            "ORDER BY sh.property_id DESC, sh.update_date DESC"
            f") AS status WHERE status_id IN ({place_holders})"
        )

        records = self.driver.query(sql=sql, args=values)

        if not records:
            return None

        return [record[0] for record in records]
