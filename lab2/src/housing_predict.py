from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib

router = APIRouter()

# Load the model
model = joblib.load("model_pipeline.pkl")

class HousingInput(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    population: float
    AveOccup: float
    latitude: float
    longitude: float

    class Config:
        extra = "forbid"

@router.post("/predict")
async def predict(input_data: HousingInput):
    try:
        # Create the input feature array in the correct order
        input_array = np.array([[
            input_data.MedInc,
            input_data.HouseAge,
            input_data.AveRooms,
            input_data.AveBedrms,
            input_data.population,
            input_data.AveOccup,
            input_data.latitude,
            input_data.longitude
        ]])

        # Perform the prediction
        prediction = model.predict(input_array)[0]
        
        return {"prediction": prediction}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
