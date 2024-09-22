from fastapi import FastAPI
from scr.housing_predict import predict_app 

app = FastAPI()

# Mount sub-application
app.mount("/predict", predict_app)