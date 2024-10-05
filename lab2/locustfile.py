from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://localhost:8000"
    @task
    def predict(self):
        self.client.post("/lab/predict", json={
            "longitude": -122.1,
            "latitude": 37.7,
            "MedInc": 5.0,
            "HouseAge": 25.0,
            "AveBedrms": 1.0,
            "AveRooms": 6.0,
            "population": 300.0,
            "AveOccup": 2.5
        })
