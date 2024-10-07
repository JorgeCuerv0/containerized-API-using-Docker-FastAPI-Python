from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import joblib

# Create the FastAPI app for prediction
predict_app = FastAPI()

# Load the pre-trained machine learning model
model = joblib.load("model_pipeline.pkl")

# Define the input data schema using Pydantic's BaseModel
class PredictionRequest(BaseModel):
    longitude: float
    latitude: float
    MedInc: float
    HouseAge: float
    AveBedrms: float
    AveRooms: float
    population: float
    AveOccup: float

    # Prevent extra fields from being passed
    class Config:
        extra = "forbid"

    # Validator for longitude
    @validator('longitude')
    def validate_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Invalid longitude')
        return v

    # Validator for latitude
    @validator('latitude')
    def validate_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Invalid latitude')
        return v

# Define the response model for predictions
class PredictionResponse(BaseModel):
    prediction: float

# Define the /predict endpoint
@predict_app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    # Extract the input data and format it for the model
    data = [
        request.longitude,
        request.latitude,
        request.MedInc,
        request.HouseAge,
        request.AveBedrms,
        request.AveRooms,
        request.population,
        request.AveOccup
    ]

    try:
        # Make the prediction using the pre-trained model
        prediction = model.predict([data])[0]  # Single prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed")

    # Return the prediction as a response
    return PredictionResponse(prediction=prediction)

# A basic health check endpoint
@predict_app.get("/health")
def health_check():
    return {"status": "healthy"}
