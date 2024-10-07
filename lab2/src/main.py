from fastapi import FastAPI
from src.housing_predict import predict_app  # Import the sub-app from housing_predict

# Create the main FastAPI app
app = FastAPI()

# Mount the sub-application under the "/lab" path
# All routes in the sub-app will now be accessed at "/lab/..."
app.mount("/lab", predict_app)
