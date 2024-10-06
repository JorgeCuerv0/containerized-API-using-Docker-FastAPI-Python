from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError, ConfigDict
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

    model_config = ConfigDict(extra='forbid')

class PredictionResponse(BaseModel):
    prediction: float

# Create FastAPI instance with the /lab prefix
predict_app = FastAPI()

# Exception handler for validation errors
@predict_app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# Health check endpoint
@predict_app.get("/health")
async def health_check():
    return {"time": datetime.now().isoformat()}

# Hello endpoint
@predict_app.get("/hello")
async def get_name(name: str = None):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    return {'message': f"Hello {name}!"}

# Prediction endpoint
@predict_app.post("/predict", response_model=PredictionResponse)
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
        return {"prediction": float(prediction)}  # Ensure prediction is always a float
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
