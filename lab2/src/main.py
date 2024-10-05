from fastapi import FastAPI
from src.housing_predict import predict_app

app = FastAPI()

# Mount the sub-application at /lab
app.mount("/lab", predict_app)
