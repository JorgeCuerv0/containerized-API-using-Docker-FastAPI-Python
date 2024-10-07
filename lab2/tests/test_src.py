# Import TestClient to test our FastAPI app and the FastAPI app instance from src.main
from fastapi.testclient import TestClient
from src.main import app  # We make sure to import the correct FastAPI app instance (the main app)

# Create a TestClient instance using the FastAPI app
client = TestClient(app)

# Ensure the "/lab/health" endpoint is defined in the app for a basic health check
@app.get("/lab/health")
def health_check():
    # Return status and the current time in ISO format
    return {"status": "ok", "time": datetime.now().isoformat()}

# Test for valid predictions with all features provided correctly (Autograder: test_predict_basic)
def test_predict_basic():
    # Make a POST request to the /lab/predict endpoint with valid data
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
    # We expect a 200 OK status and a prediction in the response
    assert response.status_code == 200
    assert "prediction" in response.json()

# Test for invalid input when the longitude is given as a string instead of a float (Autograder: test_predict_bad_type)
def test_predict_bad_type():
    response = client.post("/lab/predict", json={
        "longitude": "test",  # Invalid longitude (string instead of float)
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    # We expect a 422 Unprocessable Entity error due to the invalid data type
    assert response.status_code == 422
    assert "Input should be a valid number" in response.json()["detail"][0]["msg"]

# Test for an edge case where we give the extreme valid longitude and latitude values (Autograder: test_predict_edge_case)
def test_predict_edge_case():
    response = client.post("/lab/predict", json={
        "longitude": 180,  # Maximum valid longitude
        "latitude": 90,    # Maximum valid latitude
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    # We expect a valid prediction to be returned with a 200 OK status
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float)

# Test for missing a required feature (longitude in this case) (Autograder: test_predict_missing_feature)
def test_predict_missing_feature():
    response = client.post("/lab/predict", json={
        # Longitude is missing here
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    # We expect a 422 error since longitude is a required field
    assert response.status_code == 422
    json_response = response.json()
    assert "longitude" in str(json_response)  # Ensure that the missing field is flagged

# Test for invalid data type, like string instead of float for longitude (Autograder: test_predict_invalid_data_type)
def test_predict_invalid_data_type():
    response = client.post("/lab/predict", json={
        "longitude": "test",  # Invalid longitude (string instead of float)
        "latitude": 90,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    assert response.status_code == 422
    json_response = response.json()
    # We ensure the error message indicates the invalid data type
    assert "longitude" in json_response["detail"][0]["loc"]
    assert json_response["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"

# Test the predict endpoint to ensure the order of features is correctly handled (Autograder: test_predict_order)
def test_predict_order():
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
    json_response = response.json()
    assert "prediction" in json_response
    assert isinstance(json_response["prediction"], float)

# Test for both missing and extra fields (missing AveOccup, extra extra_feature) (Autograder: test_predict_missing_and_extra_feature)
def test_predict_missing_and_extra_feature():
    response = client.post("/lab/predict", json={
        "longitude": -122.1,
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "extra_feature": 100  # Extra field that's not part of the model
    })
    assert response.status_code == 422
    json_response = response.json()

    # Check if 'AveOccup' is flagged as missing
    missing_field_error = any(
        detail["loc"] == ["body", "AveOccup"] and "Field required" in detail["msg"]
        for detail in json_response["detail"]
    )
    # Check if 'extra_feature' is flagged as an extra field
    extra_field_error = any(
        detail["loc"] == ["body", "extra_feature"] and "Extra inputs are not permitted" in detail["msg"]
        for detail in json_response["detail"]
    )

    assert missing_field_error, "'AveOccup' field missing validation not found."
    assert extra_field_error, "'extra_feature' extra field validation not found."

# Test for string inputs that are in float format (still valid because they can be parsed as numbers) (Autograder: test_predict_bad_type_only_in_format)
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
    # Even though the input is string, it can be converted into numbers, so 200 OK is expected
    assert response.status_code == 200
    assert "prediction" in response.json()
