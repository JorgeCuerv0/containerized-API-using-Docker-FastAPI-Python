# Import the TestClient class from FastAPI, which allows us to simulate requests to the API
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the main application file
from src.main import app

# Create a TestClient instance using the FastAPI app. This allows us to send HTTP requests
# to the app and receive responses for testing purposes.
client = TestClient(app)

# This test function is responsible for checking if the /health endpoint works 
def test_health():
    # Send a GET request to the /lab/health endpoint
    response = client.get("/lab/health")
    # Assert that the status code is 200 (OK), meaning the endpoint is functioning correctly
    assert response.status_code == 200

# This test function checks the /predict endpoint with valid input data.
def test_predict_valid_input():
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
        
    assert response.status_code == 200
    # Assert that the response contains a 'prediction' field, which should hold the prediction result
    assert "prediction" in response.json()
    
# This test function checks the /predict endpoint with invalid input data.
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
    
    json_response =  response.json()
    assert "longitude" in str(json_response)
    assert "type_error.float" in str(json_response)
    
# This test function checks the /predict endpoint with edge case input data.
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

# This test function checks the /predict endpoint with missing field.
def test_missing_field():
    response = client.post("/lab/predict", json={"latitude": 90})
    assert response.status_code == 422
    json_response =  response.json()
    assert "longitude" in str(json_response)
    assert "value_error.missing" in str(json_response)

# This test function checks the /hello endpoint with missing input data.
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
    
    json_response =  response.json()
    assert "longitude" in str(json_response)
    assert "type_error.float" in str(json_response)
    
# This test function checks the /hello endpoint with valid input data.
def test_hello_valid_data():
    response = client.get("/lab/hello?name=Jorge")
    assert response.status_code == 200

# This test function checks the /hello endpoint with missing input data.
def test_hello_missing_data():
    response = client.get("/lab/hello")
    assert response.status_code == 400
    json_response =  response.json()
    assert "Name is required" in str(json_response)

# This test function checks the /hello endpoint with invalid input data.
def test_hello_invalid_data():
    response = client.get("/lab/hello?name=123")
    assert response.status_code == 200
    json_response =  response.json()
    assert "Hello 123!" in str(json_response)
