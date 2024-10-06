from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the structure of the input data and enforce validation
class PredictionRequest(BaseModel):
    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)
    MedInc: float = Field(..., gt=0)
    HouseAge: float = Field(..., gt=0)
    AveBedrms: float = Field(..., gt=0)
    AveRooms: float = Field(..., gt=0)
    population: float = Field(..., gt=0)
    AveOccup: float = Field(..., gt=0)

    class Config:
        extra = 'forbid'

class PredictionResponse(BaseModel):
    prediction: float

# Create FastAPI instance
predict_app = FastAPI()

@predict_app.get("/health")
async def health_check():
    return {"time": datetime.now().isoformat()}

@predict_app.get("/hello")
async def get_name(name: str = None):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    return {'message': f"Hello {name}!"}

@predict_app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        logger.info("Loading model...")
        model = joblib.load("model_pipeline.pkl")
    except FileNotFoundError:
        logger.error("Model file not found!")
        raise HTTPException(status_code=500, detail="Model not found")

    data = [[
        request.MedInc, request.HouseAge, request.AveRooms,
        request.AveBedrms, request.population, request.AveOccup,
        request.latitude, request.longitude
    ]]

    try:
        logger.info("Running prediction...")
        prediction = model.predict(data)[0]
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return PredictionResponse(prediction=prediction)
