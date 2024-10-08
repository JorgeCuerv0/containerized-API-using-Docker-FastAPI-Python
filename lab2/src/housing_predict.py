from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel, field_validator
import joblib
from datetime import datetime

# Router for non-prediction related routes
router = APIRouter()

# Create a separate FastAPI instance for prediction-related routes
predict_app = FastAPI()

# Load your trained model
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

    model_config = {"extra": "forbid"}  # Prevent extra fields in the input

    @field_validator('longitude')
    @classmethod
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Invalid value for Longitude')
        return v

    @field_validator('latitude')
    @classmethod
    def check_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Invalid value for Latitude')
        return v
    
# Define a health check route in the APIRouter
@router.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.now().isoformat()}

# Define the predict route in the predict_app
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
    try:
        # Extract the first prediction from the returned array
        prediction = model.predict([data])[0]  # Ensure we access the first element
        return {"status": "ok", "prediction": float(prediction)}  # Add "status" for consistency
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
