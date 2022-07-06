"""Tests for database entry update methods"""

from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from api_backend.api_backend_http_api import app

AUTH = HTTPBasicAuth(username="cdehnen", password="hireme")


def test_update_single_database_entry_good_id_good_data():
    """Succeedes in updating the database entry with id 1"""
    with TestClient(app) as client:

        updated_database_entry = {
            "city": "Düsseldorf",
            "start_date": "4/13/2013",
            "end_date": "5/18/2013",
            "price": "55.82",
            "status": "Seldom",
            "color": "#fd4e19",
        }

        response = client.put("/entry/1", json=updated_database_entry, auth=AUTH)

        assert response.status_code == 200
        assert response.json() == {
            "city": "Düsseldorf",
            "start_date": "4/13/2013",
            "end_date": "5/18/2013",
            "price": "55.82",
            "status": "Seldom",
            "color": "#fd4e19",
            "id": 1,
        }


def test_update_single_database_entry_bad_id():
    """Fails in updating the database entry because of not existing id"""
    with TestClient(app) as client:

        updated_database_entry = {
            "city": "Düsseldorf",
            "start_date": "4/13/2013",
            "end_date": "5/18/2013",
            "price": "55.82",
            "status": "Monthly",
            "color": "#fd4e19",
        }

        response = client.put("/entry/0", json=updated_database_entry, auth=AUTH)

        assert response.status_code == 404
        assert response.json() == {"message": "Entry with id 0 not found."}
