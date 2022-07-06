"""Tests for database entry create methods"""

from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from api_backend.api_backend_http_api import app

AUTH = HTTPBasicAuth(username="cdehnen", password="hireme")


def test_create_singled_database_entry_no_auth():
    """Fails to create a database entry because of missing authentication"""
    with TestClient(app) as client:
        new_database_entry = {
            "city": "Berlin",
            "start_date": "07/01/2022",
            "end_date": "07/08/2022",
            "price": "75.80",
            "status": "Yearly",
            "color": "#ffffff",
        }

        response = client.post("/entry", json=new_database_entry)

        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_create_single_database_entry_bad_data():
    """Fails to create a database entry because of missing 'city' field in data"""
    with TestClient(app) as client:
        new_database_entry = {
            "start_date": "07/01/2022",
            "end_date": "07/08/2022",
            "price": "75.80",
            "status": "Yearly",
            "color": "#ffffff",
        }

        response = client.post("/entry", json=new_database_entry, auth=AUTH)

        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "city"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }


def test_create_single_database_entry_good_data():
    """Succedes in creating a database entry"""
    with TestClient(app) as client:
        new_database_entry = {
            "city": "Berlin",
            "start_date": "07/01/2022",
            "end_date": "07/08/2022",
            "price": "75.80",
            "status": "Yearly",
            "color": "#ffffff",
        }

        response = client.post("/entry", json=new_database_entry, auth=AUTH)

        assert response.status_code == 200
