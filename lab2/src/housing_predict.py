from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
import joblib
import numpy as np

# Create a FastAPI router
router = APIRouter()

# Load the model
model = joblib.load("model_pipeline.pkl")

# Define the input model with Pydantic
class HousingInput(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    population: float
    AveOccup: float
    latitude: float
    longitude: float

    # Prevent extra fields in the input
    model_config = ConfigDict(extra="forbid")

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

        # Return the prediction rounded to 3 decimal places
        return {"prediction": round(float(prediction), 3)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

# Define `predict_app` as a router object that can be mounted in main.py
predict_app = router
