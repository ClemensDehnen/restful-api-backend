"""Repository for database access"""

from typing import List

from api_backend.dataaccess.database_gateway_interface import \
    DatabaseGatewayInterface
from api_backend.dataaccess.errors import DatabaseEntryNotFound
from api_backend.models.database_entry import (DatabaseEntry,
                                               DatabaseEntryOptional,
                                               DatabaseEntryWithId)


class DatabaseRepository:
    """Access layer in front of the database connection"""

    def __init__(self, database_gateway: DatabaseGatewayInterface) -> None:
        self.database_gateway = database_gateway

    def get_max_id_value(self) -> int:
        """Returns the highest value for the id field"""
        max_id_value = self.database_gateway.get_max_id_value()
        return max_id_value

    def get_single_database_entry(self, entry_id: int) -> DatabaseEntryOptional:
        """Returns the database entry object for the specified id"""
        single_entry_object = self.database_gateway.get_single_entry(entry_id)
        if single_entry_object is None:
            raise DatabaseEntryNotFound
        single_entry = DatabaseEntryWithId.parse_obj(single_entry_object)
        return single_entry

    def get_all_database_entries(self) -> List[DatabaseEntryWithId]:
        """Returns a list of all database entries"""
        database_entries = []
        database_entry_objects = self.database_gateway.get_all_entries()
        for database_entry_object in database_entry_objects:
            single_entry = DatabaseEntryWithId.parse_obj(database_entry_object)
            database_entries.append(single_entry)
        return database_entries

    def create_single_database_entry(
        self, new_database_entry: DatabaseEntry
    ) -> DatabaseEntryWithId:
        """Creates a database entry using the specified data"""
        new_entry_dict = new_database_entry.dict()
        new_entry_dict["id"] = self.get_max_id_value() + 1
        try:
            self.database_gateway.create_single_entry(new_entry_dict)
        except Exception as ex:
            raise Exception() from ex
        return DatabaseEntryWithId.parse_obj(new_entry_dict)

    def update_single_database_entry(
        self, entry_id: int, updated_database_entry: DatabaseEntryOptional
    ) -> bool:
        """Updates a database entry using the given data, even when incomplete"""
        update_dict = {
            key: value
            for key, value in updated_database_entry.dict().items()
            if value is not None
        }
        return self.database_gateway.update_single_entry(entry_id, update_dict)

    def delete_single_database_entry(self, entry_id: int) -> bool:
        """Deletes the entry from database where id matches"""
        return self.database_gateway.delete_single_entry(entry_id)
