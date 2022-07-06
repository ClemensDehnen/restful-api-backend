"""Tests for database entry read methods"""

from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from api_backend.api_backend_http_api import app

AUTH = HTTPBasicAuth(username="cdehnen", password="hireme")


def test_get_single_database_entry_good_id():
    """Succeedes in reading the database entry with id 10"""
    with TestClient(app) as client:

        response = client.get("/entry/10", auth=AUTH)

        assert response.status_code == 200
        assert response.json() == {
            "city": "Limoeiro do Ajuru",
            "start_date": "3/22/2015",
            "end_date": "5/13/2013",
            "price": "13.53",
            "status": "Once",
            "color": "#676c7c",
            "id": 10,
        }


def test_get_single_database_entry_bad_id():
    """Fails reading the database entry because of a non existing id"""
    with TestClient(app) as client:

        response = client.get("/entry/0", auth=AUTH)

        assert response.status_code == 404
        assert response.json() == {"message": "Entry with id 0 not found."}


def test_get_all_database_entries():
    """Succeedes in reading all database entries"""
    with TestClient(app) as client:

        response = client.get("/entries", auth=AUTH)

        assert response.status_code == 200
