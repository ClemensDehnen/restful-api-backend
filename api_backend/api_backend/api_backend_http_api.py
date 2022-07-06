""" RESTful FastAPI App exposing CRUD methods to access database data"""

import logging
import secrets
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api_backend.dataaccess.database_repository import DatabaseRepository
from api_backend.dataaccess.errors import DatabaseEntryNotFound
from api_backend.dataaccess.mongo_database_gateway import MongoDatabaseGateway
from api_backend.exceptions import ErrorMessage
from api_backend.models.database_entry import (DatabaseEntry,
                                               DatabaseEntryOptional,
                                               DatabaseEntryWithId)

app = FastAPI(title="API Backend")
security = HTTPBasic()
DATABASE_REPOSITORY: DatabaseRepository = None


def check_credentials(
    credentials: HTTPBasicCredentials = Depends(security, use_cache=False)
):
    """Test given credentials against hardcoded credentials."""

    correct_username = secrets.compare_digest(credentials.username, "cdehnen")
    correct_password = secrets.compare_digest(credentials.password, "hireme")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Create
@app.post(
    "/entry",
    summary="Create a single database entry",
    response_description="The created database entry including the new id",
    responses={500: {"model": ErrorMessage}},
    response_model=DatabaseEntryWithId,
    tags=["CREATE"],
)
def create_singles_database_entry(
    new_database_entry: DatabaseEntry,
    credentials: HTTPBasicCredentials = Depends(check_credentials, use_cache=False),
):
    """Creates a single database entry based on the given data."""

    try:
        return DATABASE_REPOSITORY.create_single_database_entry(new_database_entry)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"message": "Entry could not be written to database"},
        )


# Read
@app.get(
    "/entries",
    summary="Returns all database entries",
    response_description="A list of all database entries",
    response_model=List[DatabaseEntryWithId],
    tags=["READ"],
)
def get_all_database_entries(
    credentials: HTTPBasicCredentials = Depends(check_credentials, use_cache=False)
):
    """Returns all entries from the database"""

    return DATABASE_REPOSITORY.get_all_database_entries()


@app.get(
    "/entry/{entry_id}",
    summary="Find entry by ID",
    response_description="The database entry with all fields",
    response_model=DatabaseEntryWithId,
    responses={404: {"description": "Entry not found", "model": ErrorMessage}},
    tags=["READ"],
)
def get_single_database_entry(
    entry_id: int,
    credentials: HTTPBasicCredentials = Depends(check_credentials, use_cache=False),
):
    """Returns a single entry from the database that matches the given ID."""

    try:
        single_database_entry = DATABASE_REPOSITORY.get_single_database_entry(entry_id)
        return single_database_entry
    except DatabaseEntryNotFound:
        return JSONResponse(
            status_code=404, content={"message": f"Entry with id {entry_id} not found."}
        )


@app.get(
    "/entries/max_id",
    summary="Returns the max value of the 'id' column",
    response_description="A list of all database entries",
    response_model=int,
    tags=["READ"],
)
def get_max_id_value(
    credentials: HTTPBasicCredentials = Depends(check_credentials, use_cache=False)
):
    """Returns the max value of the 'id' column"""

    return DATABASE_REPOSITORY.get_max_id_value()


# Update
@app.put(
    "/entry/{entry_id}",
    summary="Update entry by ID",
    response_description="The updated database entry",
    response_model=DatabaseEntryWithId,
    responses={404: {"description": "Entry not found", "model": ErrorMessage}},
    tags=["UPDATE"],
)
def update_single_database_entry(
    entry_id: int,
    updated_database_entry: DatabaseEntryOptional,
    credentials: HTTPBasicCredentials = Depends(check_credentials, use_cache=False),
):
    """Updates a single entry in the database that matches the given ID."""

    try:
        DATABASE_REPOSITORY.get_single_database_entry(entry_id)
        if DATABASE_REPOSITORY.update_single_database_entry(
            entry_id, updated_database_entry
        ):
            return DATABASE_REPOSITORY.get_single_database_entry(entry_id)
    except DatabaseEntryNotFound:
        return JSONResponse(
            status_code=404, content={"message": f"Entry with id {entry_id} not found."}
        )


# Delete
@app.delete(
    "/entry/{entry_id}",
    summary="Deletes an entry from the database",
    responses={404: {"description": "Entry not found", "model": ErrorMessage}},
    tags=["DELETE"],
)
def delete_single_database_entry(
    entry_id: int,
    credentials: HTTPBasicCredentials = Depends(check_credentials, use_cache=False),
):
    """Deletes a single entry from the database that matches the given ID."""

    try:
        DATABASE_REPOSITORY.get_single_database_entry(entry_id)
        DATABASE_REPOSITORY.delete_single_database_entry(entry_id)
        return JSONResponse(
            status_code=200,
            content={"message": f"Entry with id {entry_id} was deleted."},
        )
    except DatabaseEntryNotFound:
        return JSONResponse(
            status_code=404, content={"message": f"Entry with id {entry_id} not found."}
        )


@app.on_event("startup")
async def startup():
    """Orchestrate routines on startup"""
    try:
        global DATABASE_REPOSITORY
        mongo_database_gateway = MongoDatabaseGateway()
        DATABASE_REPOSITORY = DatabaseRepository(mongo_database_gateway)
    except Exception as ex:
        logging.critical(str(ex))
        raise ex
