from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.housing_predict import router as housing_predict_router

# Create the main FastAPI app
app = FastAPI()

# Include the housing prediction router under the '/lab' prefix
app.include_router(housing_predict_router, prefix="/lab")

# Define the root endpoint to handle undefined routes
@app.get("/")
async def root():
    # Return a 404 Not Found response for the root path
    return JSONResponse(status_code=404, detail="Not Found")
