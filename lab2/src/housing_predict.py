from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

predict_app = FastAPI()

class PredictionRequest(BaseModel):
    longitude: float
    latitude: float
    MedInc: float
    HouseAge: float
    AveBedrms: float
    AveRooms: float
    population: float
    AveOccup: float

@predict_app.get("/hello")
def get_hello(name: str = None):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    return {"message": f"Hello {name}!"}

@predict_app.post("/predict")
def predict(request: PredictionRequest):
    # Assuming a model has been loaded elsewhere
    data = [[request.longitude, request.latitude, request.MedInc, request.HouseAge, request.AveBedrms, request.AveRooms, request.population, request.AveOccup]]
    prediction = 2.5  # Placeholder for model prediction logic
    return {"prediction": prediction}
