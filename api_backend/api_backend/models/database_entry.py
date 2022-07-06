"""All models needed for the Database Entry schema"""
from pydantic import BaseModel


class DatabaseEntryOptional(BaseModel):
    """Database Entry with all values defaulting to None"""

    city: str = None
    start_date: str = None
    end_date: str = None
    price: str = None
    status: str = None
    color: str = None


class DatabaseEntry(BaseModel):
    """Database Entry with all values required"""

    city: str
    start_date: str
    end_date: str
    price: str
    status: str
    color: str


class DatabaseEntryWithId(DatabaseEntryOptional):
    """Database Entry with additional 'id' attribute"""

    id: int = None
