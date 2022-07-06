"""Interface for database gateways
    Allows for interchangeability of database connectors
"""

import abc


class DatabaseGatewayInterface(abc.ABC):
    """Interface class for database gateways"""

    @abc.abstractmethod
    def get_max_id_value(self) -> int:
        """Get the highest currently used value of the 'id' column"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_single_entry(self, entry_id: int) -> dict:
        """Fetches single database object with specified 'entry_id'"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_entries(self) -> dict:
        """Fetches all database objects."""
        raise NotImplementedError()

    @abc.abstractmethod
    def create_single_entry(self, new_entry_data: dict) -> dict:
        """Creates single database object with data specified in 'new_entry_data'"""
        raise NotImplementedError()

    @abc.abstractmethod
    def update_single_entry(self, entry_id: int, update_data: dict) -> bool:
        """Overwrites single database object with specified 'entry_id' using 'update_data'"""
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_single_entry(self, entry_id: int) -> bool:
        """Deletes single database object with specified 'entry_id'"""
        raise NotImplementedError()
