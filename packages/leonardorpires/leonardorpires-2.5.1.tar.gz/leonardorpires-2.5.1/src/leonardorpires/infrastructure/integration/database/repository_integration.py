from typing import List, Optional, Union

from sqlalchemy.sql.elements import BinaryExpression

from pyiris.infrastructure.integration.database import Base
from pyiris.infrastructure.integration.database.connection_factory import Session


class RepositoryIntegration(object):
    """
    A class responsible for executing CRUD operations in the database.
    """

    def __init__(self, session=None):
        self.session: Optional[Session] = session or Session()

    def add(self, table: Base) -> Base:
        """
        Add a line in an specific table.

        :param table: A valid sqlalchemy declarative mapping object
        :type table: :class:`sqlalchemy.ext.declarative.declarative_base`

        :return: The declarative mapping object
        :rtype metadata_table: :class:`sqlalchemy.ext.declarative.declarative_base`
        """
        self.session.add(table)
        self.session.commit()
        return table

    def add_all(self, tables: List[Base]) -> Base:
        """
        Add a line in an specific table.

        :param tables: A valid sqlalchemy declarative mapping object
        :type tables: :class:`sqlalchemy.ext.declarative.declarative_base`

        :return: The declarative mapping object
        :rtype metadata_table: :class:`sqlalchemy.ext.declarative.declarative_base`
        """

        self.session.add_all(tables)
        self.session.commit()
        return tables

    def delete(self, table: Base, filter: BinaryExpression) -> Base:
        """
        Delete lines according to the filter passed on an specific table.

        :param table: A valid sqlalchemy declarative mapping object
        :type table: :class:`sqlalchemy.ext.declarative.declarative_base`

        :param filter: a valid sqlalchemy filter
        :type filter: :class:`sqlalchemy.sql.elements.BinaryExpression`

        :return: The declarative mapping object
        :rtype metadata_table: :class:`sqlalchemy.ext.declarative.declarative_base`
        """
        self.session.query(table).filter(filter).delete()
        self.session.commit()
        return table

    def get(
        self, table: Base, filter: Optional[BinaryExpression] = None
    ) -> Union[List[Base], None]:
        """
        Get all registers of an specific table in the database.

        :param table: A valid sqlalchemy declarative mapping object
        :type table: :class:`sqlalchemy.ext.declarative.declarative_base`

        :param filter: a valid sqlalchemy update value
        :type filter: optional, :class:`sqlalchemy.sql.elements.BinaryExpression`

        :return: The results of 'pyiris.infrastructure.service.metadata.Base' lines on database.
        :rtype list(dataset_metadata): :class: `~pyiris.infrastructure.service.metadata.Base`

        """
        if type(filter) == BinaryExpression:
            results = self.session.query(table).filter(filter).all()
        else:
            results = self.session.query(table).all()
        if results:
            return results
        else:
            return None

    def update(self, table: Base, filter: BinaryExpression, update_value: dict):
        """
        Update all registers of an specific table in the database according to a filter_by constraint.

        :param table: A valid sqlalchemy declarative mapping object
        :type table: :class:`sqlalchemy.ext.declarative.declarative_base`

        :param filter: a valid sqlalchemy update value
        :type filter: :class:`sqlalchemy.orm.query.Query.update`

        :param update_value: a dict with the columns and new values
        :type update_value: dict

        :return: The results of 'pyiris.infrastructure.service.metadata.Base' lines on database.
        :rtype list(dataset_metadata): :class: `~pyiris.infrastructure.service.metadata.Base`
        """
        result = self.session.query(table).filter(filter).update(update_value)
        self.session.commit()
        return result
