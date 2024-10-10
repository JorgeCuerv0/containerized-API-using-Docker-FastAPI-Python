from fastapi.testclient import TestClient
from src.main import app
from datetime import datetime

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

# Additional Test Cases

def test_hello_missing_name():
    response = client.get("/lab/hello")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["loc"] == ["query", "name"]

def test_predict_missing_fields():
    payload = {
        "MedInc": 8.3252,
        # "HouseAge": 41,  # Missing
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["loc"] == ["body", "HouseAge"]

def test_predict_invalid_data_types():
    payload = {
        "MedInc": "eight",  # Invalid type
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid float"
    assert response.json()["detail"][0]["loc"] == ["body", "MedInc"]

def test_predict_out_of_bounds_coordinates():
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 100.0,  # Invalid latitude
        "Longitude": -200.0  # Invalid longitude
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "Latitude"] and "Invalid value for Latitude" in error["msg"] for error in errors)
    assert any(error["loc"] == ["body", "Longitude"] and "Invalid value for Longitude" in error["msg"] for error in errors)

def test_predict_extra_fields():
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23,
        "ExtraField": "NotAllowed"  # Extra field
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "extra fields not permitted"
    assert response.json()["detail"][0]["loc"] == ["body", "ExtraField"]

def test_undefined_route():
    response = client.get("/undefined-route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_health_returns_valid_timestamp():
    response = client.get("/lab/health")
    assert response.status_code == 200
    time_str = response.json().get("time")
    assert time_str is not None
    try:
        datetime.fromisoformat(time_str)
    except ValueError:
        assert False, "Time is not a valid ISO8601 timestamp"

# Additional Relevant Tests

def test_predict_boundary_coordinates():
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": -90.0,       # Lower bound of latitude
        "Longitude": 180.0       # Upper bound of longitude
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float)

def test_predict_negative_values():
    payload = {
        "MedInc": -8.3252,         # Negative median income
        "HouseAge": -41,           # Negative house age
        "AveRooms": -6.9841,       # Negative average rooms
        "AveBedrms": -1.0238,      # Negative average bedrooms
        "Population": -322,        # Negative population
        "AveOccup": -2.5556,       # Negative average occupancy
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    expected_fields = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup"]
    for field in expected_fields:
        assert any(error["loc"] == ["body", field] and "Invalid value for" in error["msg"] for error in errors)

def test_predict_high_precision_floats():
    payload = {
        "MedInc": 8.32523456789,
        "HouseAge": 41.123456789,
        "AveRooms": 6.984123456789,
        "AveBedrms": 1.023456789,
        "Population": 322.123456789,
        "AveOccup": 2.5556789,
        "Latitude": 37.880123456,
        "Longitude": -122.230123456
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float)

