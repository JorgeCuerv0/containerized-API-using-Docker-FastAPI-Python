# main.py
from fastapi import FastAPI
from src.housing_predict import predict_app  # Import the sub-app from housing_predict

# Create the main FastAPI app
app = FastAPI()

# Mount the sub-application at "/lab"
app.mount("/lab", predict_app)

