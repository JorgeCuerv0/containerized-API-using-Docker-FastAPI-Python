from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
from datetime import datetime

app = FastAPI()

# Health check endpoint
@app.get("/health")
async def health_check():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"time": current_time}

# Hello endpoint
@app.get("/hello")
async def get_name(name: str = None):
    if not name:  # This will check for both None and empty string
        raise HTTPException(status_code=400, detail="Name is required")
    return {'message': f"Hello {name}!"}


# Root endpoint
@app.get("/")
async def not_found():
    raise HTTPException(status_code=404, detail="Not Found")

class PredictionRequest(BaseModel):
    longitude: float = Field(..., gt = -180, lt = 180)
    latitude: float = Field(..., gt = -90, lt = 90)
    
    @validator("longitude")
    def validate_longitude(cls, value):
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")   
        return value
    
    @validator("latitude")
    def validate_latitude(cls, value):
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90") 
        return value
    
class PredictionResponse(BaseModel):
    prediction: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Load the trained model (model_pipeline.pkl)
    model = joblib.load("model_pipeline.pkl")
    
    # Prepare the data for prediction (extract longitude and latitude)
    data = [[request.longitude, request.latitude]]
    
    #prediction
    prediction = model.predict(data)[0]
    
    # Return the prediction wrapped in a PredictionResponse model
    return PredictionResponse(prediction=prediction)
    
        
