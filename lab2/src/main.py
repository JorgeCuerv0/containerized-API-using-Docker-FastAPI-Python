from fastapi import FastAPI
from scr.housing_predict import predict 

app = FastAPI()

# Mount sub-application
app.mount("/predict", predict.app)