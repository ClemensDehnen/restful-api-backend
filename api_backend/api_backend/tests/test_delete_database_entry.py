"""Tests for database entry delete methods"""

from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from api_backend.api_backend_http_api import app

AUTH = HTTPBasicAuth(username="cdehnen", password="hireme")


def test_delete_single_database_entry_good_id():
    """Succeedes in deleting the database entry with the highest id"""
    with TestClient(app) as client:

        response = client.get("/entries/max_id", auth=AUTH)
        max_id = response.json()

        response = client.delete(f"/entry/{max_id}", auth=AUTH)

        assert response.status_code == 200
        assert response.json() == {"message": f"Entry with id {max_id} was deleted."}


def test_delete_single_database_entry_bad_id():
    """Fails in deleting a database entry because of a not existing id"""
    with TestClient(app) as client:

        response = client.delete("/entry/0", auth=AUTH)

        assert response.status_code == 404
        assert response.json() == {"message": "Entry with id 0 not found."}
