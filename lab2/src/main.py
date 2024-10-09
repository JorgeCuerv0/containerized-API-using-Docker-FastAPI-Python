from fastapi import FastAPI, HTTPException
from src.housing_predict import predict_app, router

app = FastAPI()

# Mount the predict_app as a sub-application under /lab
app.mount("/lab", predict_app)

# Include other routes like /health using APIRouter
app.include_router(router)

@app.get("/hello")
# takes a query parameter name
async def hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

