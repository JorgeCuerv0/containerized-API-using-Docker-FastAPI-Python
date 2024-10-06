from fastapi.testclient import TestClient
from src.main import app  # Import the correct FastAPI app instance (main app)

# Create a TestClient instance using the FastAPI app. This allows us to send HTTP requests
client = TestClient(app)

def test_health():
    response = client.get("/lab/health")
    assert response.status_code == 200
    assert "time" in response.json()

def test_predict_valid_basic():
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

# Test predict endpoint with invalid input
def test_predict_invalid_input():
    response = client.post("/lab/predict", json={
        "longitude": "test",
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    assert response.status_code == 422
    assert "Input should be a valid longitude as a number" in response.json()["detail"]
# Test predict with edge cases
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
    assert isinstance(response.json()["prediction"], float)

# Test predict with missing feature
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
    assert response.status_code == 422
    json_response = response.json()
    assert "longitude" in str(json_response)

# Test predict with invalid data type
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
    assert "longitude" in json_response["detail"][0]["loc"]
    assert json_response["detail"][0]["msg"] == "value is not a valid float"

# Test hello with valid data
def test_hello_valid_data():
    response = client.get("/lab/hello?name=Jorge")
    assert response.status_code == 200

# Test hello with missing data
def test_hello_missing_data():
    response = client.get("/lab/hello")
    assert response.status_code == 400
    json_response = response.json()
    assert "Name is required" in str(json_response)

# Test hello with invalid data
def test_hello_invalid_data():
    response = client.get("/lab/hello?name=123")
    assert response.status_code == 200
    json_response = response.json()
    assert "Hello 123!" in str(json_response)

# Test predict order
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

# Test predict with missing and extra feature
def test_predict_missing_and_extra_feature():
    response = client.post("/lab/predict", json={
        "longitude": -122.1,
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "extra_feature": 100
    })
    assert response.status_code == 422
    assert "Unexpected fields: extra_feature" in response.json()["detail"]
    assert "Missing required field: AveOccup" in response.json()["detail"]

# Test predict with bad data type
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
    assert response.status_code == 422

# Test predict with only formatting issues
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
    assert response.status_code == 200


