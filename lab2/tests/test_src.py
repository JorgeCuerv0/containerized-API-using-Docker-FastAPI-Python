# Import the TestClient class from FastAPI, which allows us to simulate requests to the API
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the main application file
from src.main import app

# Create a TestClient instance using the FastAPI app. This allows us to send HTTP requests
# to the app and receive responses for testing purposes.
client = TestClient(app)

# This test function is responsible for checking if the /lab/health endpoint works
def test_health():
    # Send a GET request to the /lab/health endpoint
    response = client.get("/lab/health")
    # Assert that the status code is 200 (OK), meaning the endpoint is functioning correctly
    assert response.status_code == 200
    assert "time" in response.json(), "Response does not contain 'time' field"
    assert isinstance(response.json()["time"], str), "'time' field is not of type string"


# This test function checks the /lab/predict endpoint with valid input data.
def test_predict_valid_basic():
    # Send a POST request to the /lab/predict endpoint with valid longitude and latitude
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
        
    assert response.status_code == 200, "API did not respond with a 200 code /lab/predict"
    # Assert that the response contains a 'prediction' field, which should hold the prediction result
    assert "prediction" in response.json(), "Response does not contain 'prediction' field"
    assert isinstance(response.json()["prediction"], float), "'prediction' field is not of type float"

    
# This test function checks the /lab/predict endpoint with invalid input data.
def test_predict_invalid_input():
    # Send a POST request to the /lab/predict endpoint with invalid longitude and latitude
    response = client.post("/lab/predict", json={
        "longitude": "test",  # Invalid longitude
        "latitude": 90,       # Valid latitude
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    
    # Assert that the status code is 422, which indicates a validation error occurred due to the invalid input
    assert response.status_code == 422
    
    json_response = response.json()
    assert "longitude" in str(json_response)
    assert "type_error.float" in str(json_response)  
    
# This test function checks the /lab/predict endpoint with edge case input data.
def test_predict_edge_case():
    response = client.post("/lab/predict", json={
        "longitude": 180,
        "latitude": 90,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float), "'prediction' field is not of type float"


# This test function checks the /lab/predict endpoint with missing field.
def test_predict_missing_feature():
    response = client.post("/lab/predict", json={
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    # Assert that the status code is 422, indicating a validation error for missing fields
    assert response.status_code == 422, "Endpoint did not return the correct error for missing feature"

# This test function checks the /lab/predict endpoint with invalid input data.
def test_predict_invalid_data_type():
    response = client.post("/lab/predict", json={
        "longitude": "test",
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
    assert "longitude" in str(json_response)
    assert "type_error.float" in str(json_response)
    
# This test function checks the /lab/hello endpoint with valid input data.
def test_hello_valid_data():
    response = client.get("/lab/hello?name=Jorge")
    assert response.status_code == 200

# This test function checks the /lab/hello endpoint with missing input data.
def test_hello_missing_data():
    response = client.get("/lab/hello")
    assert response.status_code == 400
    json_response = response.json()
    assert "Name is required" in str(json_response)

# This test function checks the /lab/hello endpoint with invalid input data.
def test_hello_invalid_data():
    response = client.get("/lab/hello?name=123")
    assert response.status_code == 200
    json_response = response.json()
    assert "Hello 123!" in str(json_response)
    
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
    assert "prediction" in response.json(), "Response does not contain 'prediction' field"
    assert isinstance(response.json()["prediction"], float), "'prediction' field is not of type float"

    
def test_predict_missing_and_extra_feature():
    response = client.post("/lab/predict", json={
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "extra_feature": "unexpected"
    })
    assert response.status_code == 422, "Endpoint did not return the correct error for missing and extra feature"

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
    assert response.status_code == 422, "Endpoint did not return the correct error for bad type"

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
    assert response.status_code == 200, "Endpoint did not return the correct HTTP error for bad type format"
