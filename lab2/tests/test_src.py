from fastapi.testclient import TestClient
from src.main import app
from datetime import datetime

# Create a test client using the FastAPI app
client = TestClient(app)

def test_hello():
    # Test the /lab/hello endpoint with a valid name parameter
    response = client.get("/lab/hello?name=John")
    assert response.status_code == 200  # Expect a 200 OK response
    assert response.json() == {"message": "Hello John"}  # Verify the response content

def test_health():
    # Test the /lab/health endpoint
    response = client.get("/lab/health")
    assert response.status_code == 200  # Expect a 200 OK response
    assert "time" in response.json()  # Ensure 'time' is in the response JSON

def test_predict():
    # Test the /lab/predict endpoint with valid input data
    payload = {
        "MedInc": 8.3252,      # Median income
        "HouseAge": 41,        # Median house age
        "AveRooms": 6.9841,    # Average number of rooms
        "AveBedrms": 1.0238,   # Average number of bedrooms
        "Population": 322,     # Population
        "AveOccup": 2.5556,    # Average occupancy
        "Latitude": 37.88,     # Latitude within valid range
        "Longitude": -122.23   # Longitude within valid range
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 200  # Expect a 200 OK response
    assert "prediction" in response.json()  # Check if 'prediction' is in the response
    assert isinstance(response.json()["prediction"], float)  # Ensure the prediction is a float

def test_hello_missing_name():
    # Test the /lab/hello endpoint without the 'name' parameter
    response = client.get("/lab/hello")
    assert response.status_code == 422  # Expect a 422 Unprocessable Entity
    # Verify that the error message indicates the 'name' field is required
    assert response.json()["detail"][0]["msg"] == "Field required"
    assert response.json()["detail"][0]["loc"] == ["query", "name"]

def test_predict_missing_fields():
    # Test the /lab/predict endpoint with a missing required field 'HouseAge'
    payload = {
        "MedInc": 8.3252,
        # "HouseAge": 41,  # Missing on purpose
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422  # Expect a 422 Unprocessable Entity
    # Verify that the error message indicates 'HouseAge' is required
    assert response.json()["detail"][0]["msg"] == "Field required"
    assert response.json()["detail"][0]["loc"] == ["body", "HouseAge"]

def test_predict_invalid_data_types():
    # Test the /lab/predict endpoint with an invalid data type for 'MedInc'
    payload = {
        "MedInc": "eight",  # Invalid type: should be a float
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422  # Expect a 422 Unprocessable Entity
    # Verify that the error message indicates an invalid number input
    assert "Input should be a valid number" in response.json()["detail"][0]["msg"]
    assert response.json()["detail"][0]["loc"] == ["body", "MedInc"]

def test_predict_out_of_bounds_coordinates():
    # Test the /lab/predict endpoint with invalid latitude and longitude values
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 100.0,    # Invalid latitude (> 90)
        "Longitude": -200.0   # Invalid longitude (< -180)
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422  # Expect a 422 Unprocessable Entity
    errors = response.json()["detail"]
    # Check for an error message about invalid 'Latitude'
    assert any(
        error["loc"] == ["body", "Latitude"] and "Invalid value for Latitude" in error["msg"]
        for error in errors
    )
    # Check for an error message about invalid 'Longitude'
    assert any(
        error["loc"] == ["body", "Longitude"] and "Invalid value for Longitude" in error["msg"]
        for error in errors
    )

def test_predict_extra_fields():
    # Test the /lab/predict endpoint with an extra, undefined field
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23,
        "ExtraField": "NotAllowed"  # This field should not be accepted
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422  # Expect a 422 Unprocessable Entity
    # Verify that the error message indicates extra inputs are not permitted
    assert response.json()["detail"][0]["msg"] == "Extra inputs are not permitted"
    assert response.json()["detail"][0]["loc"] == ["body", "ExtraField"]

def test_undefined_route():
    # Test an undefined route to ensure it returns a 404 Not Found
    response = client.get("/undefined-route")
    assert response.status_code == 404  # Expect a 404 Not Found
    assert response.json() == {"detail": "Not Found"}  # Verify the response content

def test_health_returns_valid_timestamp():
    # Test the /lab/health endpoint to ensure it returns a valid timestamp
    response = client.get("/lab/health")
    assert response.status_code == 200  # Expect a 200 OK response
    time_str = response.json().get("time")
    assert time_str is not None  # Ensure 'time' is in the response
    try:
        datetime.fromisoformat(time_str)  # Try parsing the timestamp
    except ValueError:
        assert False, "Time is not a valid ISO8601 timestamp"  # Fail if parsing fails

def test_predict_boundary_coordinates():
    # Test the /lab/predict endpoint with boundary latitude and longitude values
    payload = {
        "MedInc": 8.3252,
        "HouseAge": 41,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322,
        "AveOccup": 2.5556,
        "Latitude": -90.0,    # Lower bound of latitude
        "Longitude": 180.0    # Upper bound of longitude
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 200  # Expect a 200 OK response
    assert "prediction" in response.json()  # Check if 'prediction' is in the response
    assert isinstance(response.json()["prediction"], float)  # Ensure the prediction is a float

def test_predict_negative_values():
    # Test the /lab/predict endpoint with negative values where positive numbers are expected
    payload = {
        "MedInc": -8.3252,        # Negative median income
        "HouseAge": -41,          # Negative house age
        "AveRooms": -6.9841,      # Negative average rooms
        "AveBedrms": -1.0238,     # Negative average bedrooms
        "Population": -322,       # Negative population
        "AveOccup": -2.5556,      # Negative average occupancy
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = client.post("/lab/predict", json=payload)
    assert response.status_code == 422  # Expect a 422 Unprocessable Entity
    errors = response.json()["detail"]
    expected_fields = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup"]
    # Check that each negative field has an appropriate error message
    for field in expected_fields:
        assert any(
            error["loc"] == ["body", field] and f"Invalid value for {field}, must be greater than zero" in error["msg"]
            for error in errors
        )

def test_predict_high_precision_floats():
    # Test the /lab/predict endpoint with high-precision float values
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
    assert response.status_code == 200  # Expect a 200 OK response
    assert "prediction" in response.json()  # Check if 'prediction' is in the response
    assert isinstance(response.json()["prediction"], float)  # Ensure the prediction is a float
