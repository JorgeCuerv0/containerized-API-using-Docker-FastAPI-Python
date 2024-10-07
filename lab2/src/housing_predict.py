from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel, field_validator
from datetime import datetime

# Create the FastAPI instance
predict_app = FastAPI()

# Load your trained model (make sure the path is correct)
model = joblib.load("model_pipeline.pkl")

# Define the input data schema using Pydantic's BaseModel
class PredictionRequest(BaseModel):
    longitude: float
    latitude: float
    MedInc: float
    HouseAge: float
    AveBedrms: float
    AveRooms: float
    population: float
    AveOccup: float

    # Prevent extra fields in the input
    model_config = {"extra": "forbid"}

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

# The POST endpoint to predict the house price based on the input features
@predict_app.post("/lab/predict")
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
        prediction = model.predict([data])  # Make sure this returns an array-like structure
        return {"prediction": float(prediction[0])}  # Return the prediction as a float
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@predict_app.get("/health")
def health_check():
    return {"status": "ok", "time": int(datetime.now().timestamp())}  # Return epoch time
