from fastapi import FastAPI
from src.housing_predict import predict_app

# Create the main FastAPI app
app = FastAPI()

# Mount the sub-application (you can adjust the route)
app.mount("/lab", predict_app)

# Optionally, expose /predict directly without /lab if tests expect it
app.include_router(predict_app)
