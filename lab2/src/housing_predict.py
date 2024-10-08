from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
import logging
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
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    model_config = ConfigDict(extra="forbid")

# Add logging configuration at the start of your script
logging.basicConfig(level=logging.DEBUG)

@router.post("/predict")
async def predict(input_data: HousingInput):
    try:
        # Log the incoming data
        logging.debug(f"Received input data: {input_data}")

        # Create the input feature array in the correct order
        input_array = np.array([[
            input_data.MedInc,
            input_data.HouseAge,
            input_data.AveRooms,
            input_data.AveBedrms,
            input_data.Population,
            input_data.AveOccup,
            input_data.Latitude,
            input_data.Longitude
        ]])

        # Log the input array for debugging
        logging.debug(f"Input array: {input_array}")

        # Perform the prediction
        prediction = model.predict(input_array)[0]

        # Log the prediction result
        logging.debug(f"Prediction result: {prediction}")

        return {"prediction": round(float(prediction), 3)}
    
    except Exception as e:
        # Log the error details
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

# Define `predict_app` as a router object that can be mounted in main.py
predict_app = router
