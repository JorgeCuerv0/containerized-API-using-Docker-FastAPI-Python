from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, validator
import joblib

# Create the sub-application
predict_app = FastAPI()

# Load your trained model (ensure this path is correct)
model = joblib.load("model_pipeline.pkl")

class PredictionRequest(BaseModel):
    longitude: float
    latitude: float
    MedInc: float
    HouseAge: float
    AveBedrms: float
    AveRooms: float
    population: float
    AveOccup: float

    @validator('longitude')
    def check_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Invalid value for Longitude')
        return v

    @validator('latitude')
    def check_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Invalid value for Latitude')
        return v

@predict_app.post("/predict")
def get_prediction(request: PredictionRequest):
    # Validate the input data
    try:
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
        # Make the prediction
        prediction = model.predict([data])
        return {"prediction": prediction[0]}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during prediction")
