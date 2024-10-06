# Import to create the API and handle errors
from fastapi import FastAPI, HTTPException
# Import to create models for request and response validation
from pydantic import BaseModel
from pydantic import Field
# Import load the machine learning model 
import joblib
# Import that allows us to get the current date and time
from datetime import datetime

# Create a new FastAPI instance that will serve as the sub-application for predictions
predict_app = FastAPI()

# Health check endpoint
# This endpoint returns the current time in ISO format.
@predict_app.get("/health")
async def health_check():
    return {"time": datetime.now().isoformat()}

# Hello endpoint
# This endpoint greets the user by name. If no name is provided, it raises a 400 Bad Request error.
@predict_app.get("/hello")
async def get_name(name: str = None):
    if not name:  # This will check for both None and empty string
        raise HTTPException(status_code=400, detail="Name is required")
    return {'message': f"Hello {name}!"}


# Root endpoint
# This endpoint is a placeholder that always returns a 404 Not Found error.
@predict_app.get("/")
async def not_found():
    raise HTTPException(status_code=404, detail="Not Found")

# This class defines the structure of the input data (longitude and latitude) and enforces constraints on their values.
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
           
# This class defines the structure of the prediction result).
class PredictionResponse(BaseModel):
    prediction: float

#This is the core functionality of the API. It takes a JSON input with longitude and latitude values,
# processes it through a pre-trained machine learning model, and returns a prediction.
@predict_app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Load the trained model (model_pipeline.pkl)
    model = joblib.load("model_pipeline.pkl")
    
    # Prepare the data for prediction (extract longitude and latitude)
    data = [[
        request.MedInc, request.HouseAge, request.AveRooms,
        request.AveBedrms, request.population, request.AveOccup,
        request.latitude, request.longitude
    ]]
    
    #prediction
    prediction = model.predict(data)[0]
    
    # Return the prediction wrapped in a PredictionResponse model
    return PredictionResponse(prediction=prediction)
    
        
