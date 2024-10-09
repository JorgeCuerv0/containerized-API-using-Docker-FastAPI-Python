from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.housing_predict import router as housing_predict_router

app = FastAPI()

# Mount the housing_predict sub-application under the /lab prefix
app.include_router(housing_predict_router, prefix="/lab")

# Root endpoint to handle undefined routes
@app.get("/")
async def root():
    return JSONResponse(status_code=404, detail="Not Found")
