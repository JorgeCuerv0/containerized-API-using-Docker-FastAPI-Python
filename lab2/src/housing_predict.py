from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, field_validator, ConfigDict
import numpy as np
import joblib
from datetime import datetime

# Create a router for the housing prediction endpoints
router = APIRouter()

# Load the pre-trained machine learning model
model = joblib.load("model_pipeline.pkl")

class HousingInput(BaseModel):
    # Define the input data model with field descriptions
    MedInc: float = Field(..., description="Median income in block group")
    HouseAge: float = Field(..., description="Median house age in block group")
    AveRooms: float = Field(..., description="Average number of rooms per household")
    AveBedrms: float = Field(..., description="Average number of bedrooms per household")
    Population: float = Field(..., description="Population in block group")
    AveOccup: float = Field(..., description="Average household size")
    Latitude: float = Field(..., description="Latitude must be between -90 and 90")
    Longitude: float = Field(..., description="Longitude must be between -180 and 180")

    # Validator to ensure that certain fields have positive values
    @field_validator('MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup')
    def check_positive(cls, value, info):
        if value <= 0:
            raise ValueError(f'Invalid value for {info.field_name}, must be greater than zero')
        return value

    # Validator for Latitude to ensure it's within -90 and 90
    @field_validator('Latitude')
    def check_latitude(cls, value):
        if not (-90 <= value <= 90):
            raise ValueError('Invalid value for Latitude')
        return value

    # Validator for Longitude to ensure it's within -180 and 180
    @field_validator('Longitude')
    def check_longitude(cls, value):
        if not (-180 <= value <= 180):
            raise ValueError('Invalid value for Longitude')
        return value

    model_config = ConfigDict(extra='forbid')  # Disallow extra fields in the input

class PredictionOutput(BaseModel):
    # Define the output data model
    prediction: float

@router.post("/predict", response_model=PredictionOutput)
async def predict(data: HousingInput):
    # Prepare the input data for the model
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

    # Make a prediction using the pre-trained model
    prediction = model.predict(input_array)
    # Return the prediction wrapped in the output data model
    return PredictionOutput(prediction=prediction[0])

@router.get("/hello")
async def hello(name: str = Query(..., description="The name to greet")):
    # A simple greeting endpoint
    return {"message": f"Hello {name}"}

@router.get("/health")
async def health():
    # A health check endpoint that returns the current UTC time
    return {"time": datetime.utcnow().isoformat()}
