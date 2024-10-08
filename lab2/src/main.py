from fastapi import FastAPI, HTTPException
from src.housing_predict import predict_app, router

app = FastAPI()

# Mount the predict_app as a sub-application under /lab
app.mount("/lab", predict_app)

# Include other routes like /health using APIRouter
app.include_router(router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Hello endpoint (for testing)
@app.get("/hello")
async def get_name(name: str = None):
    if not name:  # This will check for both None and empty string
        raise HTTPException(status_code=400, detail="Name is required")
    return {'message': f"Hello {name}!"}
