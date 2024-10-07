# housing_predict.py

from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel, field_validator

# Create the sub-application
predict_app = FastAPI()

# Load your trained model (ensure this path is correct)
model = joblib.load("model_pipeline.pkl")

class PredictionRequest(BaseModel):
    longitude: float
    latitude: float
    MedInc: float
    HouseAge: float
    AveBedrms: float
    AveRooms: float
    population: float
    AveOccup: float

    class Config:
        extra = "forbid"  # Prevent extra fields from being passed in the request body

    @field_validator('longitude')
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Invalid value for Longitude')
        return v

    @field_validator('latitude')
    def check_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Invalid value for Latitude')
        return v

@predict_app.post("/predict")
def get_prediction(request: PredictionRequest):
    data = [
        request.longitude,
        request.latitude,
        request.MedInc,
        request.HouseAge,
        request.AveBedrms,
        request.AveRooms,
        request.population,
        request.AveOccup
    ]
    prediction = model.predict([data])
    return {"prediction": prediction[0]}

# Define hello and health routes at the correct level
@predict_app.get("/hello")
def get_hello(name: str = None):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    return {"message": f"Hello {name}!"}

@predict_app.get("/health")
def health_check():
    return {"status": "healthy"}
