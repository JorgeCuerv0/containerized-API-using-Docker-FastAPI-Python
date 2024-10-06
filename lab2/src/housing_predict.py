from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError, ConfigDict
import joblib
from datetime import datetime
from typing import Dict, Any

class PredictionRequest(BaseModel):
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (between -180 and 180)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (between -90 and 90)")
    MedInc: float = Field(..., gt=0, description="Median income in block group")
    HouseAge: float = Field(..., gt=0, description="Median house age in block group")
    AveRooms: float = Field(..., gt=0, description="Average number of rooms")
    AveBedrms: float = Field(..., gt=0, description="Average number of bedrooms")
    population: float = Field(..., gt=0, description="Block group population")
    AveOccup: float = Field(..., gt=0, description="Average house occupancy")

    model_config = ConfigDict(extra='forbid')

class PredictionResponse(BaseModel):
    prediction: float

predict_app = FastAPI()

@predict_app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    error_messages = []
    for error in exc.errors():
        field = error["loc"][0]
        if error["type"] == "value_error.missing":
            error_messages.append(f"Missing required field: {field}")
        elif error["type"] == "value_error.number.not_gt":
            error_messages.append(f"Input should be a valid {field} greater than 0")
        elif "value_error.number" in error["type"]:
            error_messages.append(f"Input should be a valid {field} as a number")
        elif error["type"] == "value_error.extra":
            error_messages.append(f"Unexpected fields: {field}")
        else:
            error_messages.append(f"Invalid {field}: {error['msg']}")
    
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages}
    )

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
        return {"prediction": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
