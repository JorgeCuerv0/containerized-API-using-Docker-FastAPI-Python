from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Test the /health endpoint to ensure it returns a 200 status and "healthy" message
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "healthy"

# Test the /hello endpoint when a valid name is provided
def test_hello_with_name():
    response = client.get("/hello?name=John")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello John!"}

# Test the /hello endpoint when the name parameter is missing
def test_missing_name():
    response = client.get("/hello")
    assert response.status_code == 400
    assert response.json() == {"detail": "Name is required"}

# Test for valid predictions
def test_predict_basic():
    response = client.post("/lab/predict", json={
        "longitude": -122.1,
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    assert response.status_code == 200
    assert "prediction" in response.json()

# Test for missing and extra fields
def test_predict_missing_and_extra_feature():
    response = client.post("/lab/predict", json={
        "longitude": -122.1,
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "extra_feature": 100  # Extra field not part of the model
    })
    assert response.status_code == 422

# Test for invalid data types
def test_predict_bad_type():
    response = client.post("/lab/predict", json={
        "longitude": "not_a_float",  # Invalid type
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    assert response.status_code == 422

# Test for string inputs that can be parsed to floats
def test_predict_bad_type_only_in_format():
    response = client.post("/lab/predict", json={
        "longitude": "-122.1",
        "latitude": "37.7",
        "MedInc": "5.0",
        "HouseAge": "25.0",
        "AveBedrms": "1.0",
        "AveRooms": "6.0",
        "population": "300.0",
        "AveOccup": "2.5"
    })
    assert response.status_code == 200, "Expected 200 OK for parsable strings as numbers."
    assert "prediction" in response.json()
