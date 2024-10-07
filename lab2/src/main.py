from fastapi import FastAPI
from src.housing_predict import predict_app, router

app = FastAPI()

# Mount the predict_app as a sub-application under /lab
app.mount("/lab", predict_app)

# Include other routes like /health using APIRouter
app.include_router(router)
