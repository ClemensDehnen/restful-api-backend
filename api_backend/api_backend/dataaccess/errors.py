"""Project specific errors"""


class DatabaseEntryNotFound(Exception):
    """Raise when searched entry can not be found in database."""
