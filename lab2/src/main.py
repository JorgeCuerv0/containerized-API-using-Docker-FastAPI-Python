from fastapi import FastAPI
from src.housing_predict import predict_app

app = FastAPI()

# Mount the predict app with the prefix '/lab'
app.mount("/lab", predict_app)
