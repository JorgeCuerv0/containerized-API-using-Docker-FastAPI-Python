from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
from datetime import datetime

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

# Create FastAPI instance with the /lab prefix
predict_app = FastAPI()

# Health check endpoint
@predict_app.get("/lab/health")
async def health_check():
    return {"time": datetime.now().isoformat()}

# Hello endpoint
@predict_app.get("/lab/hello")
async def get_name(name: str = None):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    return {'message': f"Hello {name}!"}

# Root endpoint for not found
@predict_app.get("/lab/")
async def not_found():
    raise HTTPException(status_code=404, detail="Not Found")

# Prediction endpoint
@predict_app.post("/lab/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        model = joblib.load("model_pipeline.pkl")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model not found")
    
    data = [[
        request.MedInc, request.HouseAge, request.AveRooms,
        request.AveBedrms, request.population, request.AveOccup,
        request.latitude, request.longitude
    ]]
    
    try:
        prediction = model.predict(data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
    return PredictionResponse(prediction=prediction)
