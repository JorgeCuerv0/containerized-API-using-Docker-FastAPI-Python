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

# Test the /hello endpoint with an empty name
def test_no_name():
    response = client.get("/hello?name=")
    assert response.status_code == 400
    assert response.json() == {"detail": "Name is required"}

# Test the root endpoint ("/") for 404 error
def test_root_not_found():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

# Test access to the /docs endpoint
def test_docs_access():
    response = client.get("/docs")
    assert response.status_code == 200

# Test access to the OpenAPI JSON specification
def test_openapi_access():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()  # Ensure the OpenAPI key is present

# Test the /hello endpoint with a name containing special characters
def test_special_characters():
    response = client.get("/hello?name=John%20Doe")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello John Doe!"}

# Test that POST requests to the /hello endpoint return a 405 Method Not Allowed error
def test_hello_post_not_allowed():
    response = client.post("/hello")
    assert response.status_code == 405

# Test the /hello endpoint with unexpected query parameters
def test_health_with_query_parameters():
    response = client.get("/health?foo=bar")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Test the /hello endpoint with a very long name
def test_hello_long_name():
    long_name = "John" * 100  # Create a very long name string
    response = client.get(f"/hello?name={long_name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {long_name}!"}

# Test for valid predictions
def test_predict_basic():
    response = client.post("/lab/predict", json={
        "Longitude": -122.1,
        "Latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "Population": 300.0,
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
        "Longitude": "-122.1",  # String, but parsable
        "Latitude": "37.7",     # String, but parsable
        "MedInc": "5.0",
        "HouseAge": "25.0",
        "AveBedrms": "1.0",
        "AveRooms": "6.0",
        "Population": "300.0",
        "AveOccup": "2.5"
    })
    assert response.status_code == 200, "Expected 200 OK for parsable strings as numbers."
    assert "prediction" in response.json()
    


