from fastapi.testclient import TestClient
from api.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_predict_success():
    payload = {
        "data": [
            {
                "longitude": -122.23,
                "latitude": 37.88,
                "housing_median_age": 41,
                "total_rooms": 880,
                "total_bedrooms": 129,
                "population": 322,
                "households": 126,
                "median_income": 8.3252,
                "ocean_proximity": "NEAR BAY"
            }
        ]
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

        assert response.status_code == 200
        body = response.json()

        assert "predictions" in body
        assert isinstance(body["predictions"], list)
        assert len(body["predictions"]) == 1


def test_predict_invalid_input():
    payload = {
        "data": [
            {
                "latitude": 37.88,
                "housing_median_age": 41,
                "total_rooms": 880,
                "total_bedrooms": 129,
                "population": 322,
                "households": 126,
                "median_income": 8.3252,
                "ocean_proximity": "NEAR BAY"
            }
        ]
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
