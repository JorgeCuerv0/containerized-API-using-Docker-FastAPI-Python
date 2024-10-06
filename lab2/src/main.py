from fastapi import FastAPI
from src.housing_predict import predict_app

app = FastAPI()

# Mount the predict_app under the /lab path
app.mount("/lab", predict_app)
