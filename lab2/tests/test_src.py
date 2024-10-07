# Import TestClient to test our FastAPI app and the FastAPI app instance from src.main
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Test for valid predictions with all features provided correctly (Autograder: test_predict_basic)
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
    # Debug response logging
    print("Response for test_predict_basic:", response.json())
    assert response.status_code == 200, "API did not respond with 200 code."
    assert "prediction" in response.json(), "Prediction key missing in response."

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
    print("Response for test_predict_order:", response.json())
    assert response.status_code == 200
    assert "prediction" in response.json(), "Prediction key missing in response."

# Test for both missing and extra fields (Autograder: test_predict_missing_and_extra_feature)
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
    print("Response for test_predict_missing_and_extra_feature:", response.json())
    assert response.status_code == 422, "Expected 422 status code for missing or extra features."
    
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

# Test for invalid types (Autograder: test_predict_bad_type)
def test_predict_bad_type():
    response = client.post("/lab/predict", json={
        "longitude": "not_a_float",
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    print("Response for test_predict_bad_type:", response.json())
    assert response.status_code == 422, "Expected 422 status code for invalid data types."

# Test for string inputs that can be converted to floats (Autograder: test_predict_bad_type_only_in_format)
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
    print("Response for test_predict_bad_type_only_in_format:", response.json())
    assert response.status_code == 200, "Expected 200 OK for parsable strings as numbers."
    assert "prediction" in response.json()
