from fastapi.testclient import TestClient
from src.main import app  # We make sure to import the correct FastAPI app instance (the main app)

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
    # Print the response for debugging in case it fails
    print("Response for test_predict_basic: ", response.json())
    
    # Ensure the API responds with status code 200 and includes a prediction
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
    # Print the response for debugging in case it fails
    print("Response for test_predict_order: ", response.json())
    
    # Ensure the API responds with status code 200 and includes a prediction
    assert response.status_code == 200
    assert "prediction" in response.json(), "Prediction key missing in response."

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
    
    # Print the response for debugging
    print("Response for test_predict_missing_and_extra_feature: ", response.json())
    
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

# Test for invalid types (strings where floats are expected) (Autograder: test_predict_bad_type)
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
    # Print the response for debugging
    print("Response for test_predict_bad_type: ", response.json())
    
    # The API should return a 422 error due to incorrect data type
    assert response.status_code == 422

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
    # Print the response for debugging
    print("Response for test_predict_bad_type_only_in_format: ", response.json())
    
    # Even though the input is string, it can be converted into numbers, so 200 OK is expected
    assert response.status_code == 200
    assert "prediction" in response.json()
