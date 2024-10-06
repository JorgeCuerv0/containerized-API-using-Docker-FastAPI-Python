from fastapi import FastAPI
from src.housing_predict import predict_app

# Create the main FastAPI instance
app = FastAPI()

# Mount the sub-application for the /lab endpoint
app.mount("/lab", predict_app)
