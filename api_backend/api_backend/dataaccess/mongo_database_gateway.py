"""Gateway for a MongoDB"""

import logging

from pymongo import ASCENDING, DESCENDING, MongoClient

from api_backend.dataaccess.database_gateway_interface import \
    DatabaseGatewayInterface


class MongoDatabaseGateway(DatabaseGatewayInterface):
    """Database gateway using MongoDB as persistency.
    Implements IDatabaseGateway.
    """

    def __init__(self) -> None:
        super().__init__()
        self.client = MongoClient("mongodb://mongo_db/test")
        self.database = self.client.test

    def get_max_id_value(self):
        max_id_entry = (
            self.database.testCollection.find().sort("id", DESCENDING).limit(1)
        )
        return max_id_entry[0]["id"]

    def get_single_entry(self, entry_id: int):
        return self.database.testCollection.find_one({"id": entry_id})

    def get_all_entries(self):
        return self.database.testCollection.find().sort("id", ASCENDING)

    def create_single_entry(self, new_entry_data: dict):
        try:
            self.database.testCollection.insert_one(new_entry_data)
            return new_entry_data
        except Exception as exc:
            logging.error(msg=f"{exc}")
            raise Exception() from exc

    def update_single_entry(self, entry_id: int, update_data: dict):
        try:
            self.database.testCollection.update_one(
                {"id": entry_id}, {"$set": update_data}
            )
            return True
        except Exception as exc:
            logging.error(msg=f"{exc}")
            return False

    def delete_single_entry(self, entry_id: int):
        try:
            self.database.testCollection.delete_one({"id": entry_id})
            return True
        except Exception as exc:
            logging.error(msg=f"{exc}")
            return False
