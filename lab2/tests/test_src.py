from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Test the /health endpoint to ensure it returns a 200 status and "healthy" message
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    
    # Assert that the status is 'ok' and the time field is present in the response
    assert json_response["status"] == "ok"
    assert "time" in json_response

    
# Test the /hello endpoint when a valid name is provided, checking for a successful response and correct message
def test_hello_with_name():
    response = client.get("/hello?name=John")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello John!"}
    
# Test the /hello endpoint when the name parameter is missing, expecting a 400 error and "Name is required" message
def test_missing_name():
    response = client.get("/hello")
    assert response.status_code == 400
    assert response.json() == {"detail": "Name is required"}

# Test the prediction endpoint with valid input (Autograder: test_predict_basic)
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
    assert response.status_code == 200, "API did not respond with 200 code."
    assert "prediction" in response.json(), "Prediction key missing in response."

# Test the prediction endpoint with reordered input (Autograder: test_predict_order)
def test_predict_order():
    response = client.post("/lab/predict", json={
        "MedInc": 5.0,
        "latitude": 37.7,
        "longitude": -122.1,
        "HouseAge": 25.0,
        "AveRooms": 6.0,
        "AveBedrms": 1.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    assert response.status_code == 200
    assert "prediction" in response.json(), "Prediction key missing in response."

# Test for missing and extra fields (Autograder: test_predict_missing_and_extra_feature)
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
    assert response.status_code == 422, "Expected 422 status code for missing or extra features."
    
    json_response = response.json()
    missing_field_error = any(
        detail["loc"] == ["body", "AveOccup"] and "Field required" in detail["msg"]
        for detail in json_response["detail"]
    )
    extra_field_error = any(
        detail["loc"] == ["body", "extra_feature"] and "Extra inputs are not permitted" in detail["msg"]
        for detail in json_response["detail"]
    )

    assert missing_field_error, "'AveOccup' field missing validation not found."
    assert extra_field_error, "'extra_feature' extra field validation not found."

# Test for invalid data types (Autograder: test_predict_bad_type)
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
    assert response.status_code == 422, "Expected 422 status code for invalid data types."

# Test for string inputs that can be parsed to floats (Autograder: test_predict_bad_type_only_in_format)
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
