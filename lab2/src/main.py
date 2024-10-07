import logging
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/lab/health")
def health_check():
    logger.info("Health check endpoint hit")
    return {"status": "healthy"}
