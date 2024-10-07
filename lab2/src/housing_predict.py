from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel, field_validator

# Create the sub-application for housing price prediction
predict_app = FastAPI()

# Load the machine learning model
model = joblib.load("model_pipeline.pkl")

# Define the input data schema using Pydantic's BaseModel
class PredictionRequest(BaseModel):
    longitude: float  # Longitude of the location
    latitude: float   # Latitude of the location
    MedInc: float     # Median income in the area
    HouseAge: float   # Median age of the houses
    AveBedrms: float  # Average number of bedrooms per house
    AveRooms: float   # Average number of rooms per house
    population: float # Population in the area
    AveOccup: float   # Average number of occupants per household

    # Prevent any extra fields from being passed in 
    class Config:
        extra = "forbid"

    # Ensures it falls within the valid range
    @field_validator('longitude')
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Invalid value for Longitude')
        return v

    # Ensures it falls within the valid range
    @field_validator('latitude')
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
    
    # Use the model to make a prediction
    prediction = model.predict([data])

    # Return the prediction as part of the response
    return {"prediction": float(prediction[0])}

# The "hello" endpoint returns a greeting message
@predict_app.get("/hello")
def get_hello(name: str = None):
    if not name:
        # If no name is provided, raise a 400 error
        raise HTTPException(status_code=400, detail="Name is required")
    return {"message": f"Hello {name}!"}

# A health check endpoint tells us the service is running properly
@predict_app.get("/health")
def health_check():
    return {"status": "healthy"}
