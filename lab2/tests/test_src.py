from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_hello():
    response = client.get("/lab/hello?name=John")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello John"}

def test_health():
    response = client.get("/lab/health")
    assert response.status_code == 200
    assert "time" in response.json()

def test_predict():
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float)
