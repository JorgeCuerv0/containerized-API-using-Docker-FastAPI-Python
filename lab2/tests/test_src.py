from fastapi.testclient import TestClient
from src.housing_predict import predict_app

client = TestClient(predict_app)

# This test function is responsible for checking if the /health endpoint works
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "time" in response.json(), "Response does not contain 'time' field"
    assert isinstance(response.json()["time"], str), "'time' field is not of type string"


def test_predict_valid_basic():
    response = client.post("/predict", json={
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


def test_predict_invalid_input():
    response = client.post("/predict", json={
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
    assert "float_parsing" in str(json_response)


def test_predict_edge_case():
    response = client.post("/predict", json={
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


def test_predict_missing_feature():
    response = client.post("/predict", json={
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    assert response.status_code == 422, "Endpoint did not return the correct error for missing feature"


def test_predict_invalid_data_type():
    response = client.post("/predict", json={
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
    assert "float_parsing" in str(json_response)


# Check the /hello endpoint with valid data
def test_hello_valid_data():
    response = client.get("/hello?name=Jorge")
    assert response.status_code == 200
    assert "Hello Jorge!" in response.json()["message"]


# Check the /hello endpoint with missing data
def test_hello_missing_data():
    response = client.get("/hello")
    assert response.status_code == 400
    assert "Name is required" in response.json()["detail"]


# Check the /hello endpoint with invalid data
def test_hello_invalid_data():
    response = client.get("/hello?name=123")
    assert response.status_code == 200
    assert "Hello 123!" in response.json()["message"]


def test_predict_order():
    response = client.post("/predict", json={
        "longitude": -122.1,
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
    })
    assert response.status_code == 200, "API did not respond with a 200 code"
    json_response = response.json()
    assert "prediction" in json_response, "Response does not contain 'prediction' field"
    assert isinstance(json_response["prediction"], float), "'prediction' field is not of type float"


def test_predict_missing_and_extra_feature():
    response = client.post("/predict", json={
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
    response = client.post("/predict", json={
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
    response = client.post("/predict", json={
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
