from fastapi import FastAPI
from src.housing_predict import predict_app

# Main app
app = FastAPI()

# Mounting the sub-application for the predict endpoint
app.mount("/lab", predict_app)
