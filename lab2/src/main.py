from fastapi import FastAPI, HTTPException
from src.housing_predict import predict_app, router

app = FastAPI()

# Mount the predict_app as a sub-application under /lab
app.mount("/lab", predict_app)

# Include other routes like /health using APIRouter
app.include_router(router)

@app.get("/hello/{name}")
async def hello(name: str):
    if len(name) > 100:  # Example limit for long names
        raise HTTPException(status_code=400, detail="Name is too long")
    return {"message": f"Hello {name}!"}  # Ensure correct greeting format

@app.get("/hello/")
async def hello_no_name(name: str = None):
    if name is None or name == "":
        raise HTTPException(status_code=400, detail="Name is required")
    return {"message": f"Hello {name}!"}  # Ensure correct greeting format


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return JSONResponse(status_code = 404, detail = "Not Found")
