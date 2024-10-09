from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict
import numpy as np
import joblib
from datetime import datetime

router = APIRouter()

# Load the pre-trained machine learning model
model = joblib.load("model_pipeline.pkl")

class HousingInput(BaseModel):
    MedInc: float = Field(..., description="Median income in block group")
    HouseAge: float = Field(..., description="Median house age in block group")
    AveRooms: float = Field(..., description="Average number of rooms per household")
    AveBedrms: float = Field(..., description="Average number of bedrooms per household")
    Population: float = Field(..., description="Population in block group")
    AveOccup: float = Field(..., description="Average household size")
    Latitude: float = Field(..., description="Latitude must be between -90 and 90")
    Longitude: float = Field(..., description="Longitude must be between -180 and 180")

    model_config = ConfigDict(extra="forbid")  # Disallow extra fields

    @field_validator('Latitude')
    def validate_latitude(cls, value):
        if not (-90 <= value <= 90):
            raise ValueError("Invalid value for Latitude")
        return value

    @field_validator('Longitude')
    def validate_longitude(cls, value):
        if not (-180 <= value <= 180):
            raise ValueError("Invalid value for Longitude")
        return value

class PredictionOutput(BaseModel):
    prediction: float

@router.post("/predict", response_model=PredictionOutput)
async def predict(data: HousingInput):
    input_array = np.array([[
        data.MedInc,
        data.HouseAge,
        data.AveRooms,
        data.AveBedrms,
        data.Population,
        data.AveOccup,
        data.Latitude,
        data.Longitude
    ]])

    prediction = model.predict(input_array)
    return PredictionOutput(prediction=prediction[0])

@router.get("/hello")
async def hello(name: str = Query(..., description="The name to greet")):
    return {"message": f"Hello {name}"}

@router.get("/health")
async def health():
    return {"time": datetime.utcnow().isoformat()}
