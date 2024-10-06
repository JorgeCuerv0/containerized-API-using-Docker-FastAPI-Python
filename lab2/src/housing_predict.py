from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib

# Create a new FastAPI instance
predict_app = FastAPI()

# Define the input model for the prediction request
class PredictionRequest(BaseModel):
    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)
    MedInc: float = Field(..., gt=0)
    HouseAge: float = Field(..., gt=0)
    AveBedrms: float = Field(..., gt=0)
    AveRooms: float = Field(..., gt=0)
    population: float = Field(..., gt=0)
    AveOccup: float = Field(..., gt=0)

# Define a health check endpoint
@predict_app.get("/health")
def health_check():
    return {"status": "ok"}

# Define the prediction endpoint
@predict_app.post("/predict")
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
