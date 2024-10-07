from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel, field_validator

# Create the FastAPI instance
predict_app = FastAPI()

# Load your trained model
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

    model_config = {"extra": "forbid"}  # Prevent extra fields in the input

    @field_validator('longitude')
    @classmethod
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Invalid value for Longitude')
        return v

    @field_validator('latitude')
    @classmethod
    def check_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Invalid value for Latitude')
        return v

# The POST endpoint to predict the house price based on the input features
@predict_app.post("/predict")
def get_prediction(request: PredictionRequest):
    # Collect the data from the request and format it for the model
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
    
    # Use the pre-trained model to make a prediction
    try:
        prediction = model.predict([data])
        # Ensure the output is always a float and format it in a JSON object
        return {"prediction": float(prediction[0])}
    except Exception as e:
        # If prediction fails, return a 400 error
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

# Health check endpoint
@predict_app.get("/health")
def health_check():
    return {"status": "healthy"}
