from fastapi import FastAPI
from src.housing_predict import predict_app

# Create the main FastAPI app
app = FastAPI()

# Mount the sub-application for predictions at /lab
app.mount("/lab", predict_app)
