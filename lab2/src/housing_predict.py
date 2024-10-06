# Health check endpoint
@predict_app.get("/health")
async def health_check():
    return {"time": datetime.now().isoformat()}

# Hello endpoint
@predict_app.get("/hello")
async def get_name(name: str = None):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    return {'message': f"Hello {name}!"}

# Prediction endpoint
@predict_app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        model = joblib.load("model_pipeline.pkl")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model not found")

    data = [[
        request.MedInc, request.HouseAge, request.AveRooms,
        request.AveBedrms, request.population, request.AveOccup,
        request.latitude, request.longitude
    ]]

    try:
        prediction = model.predict(data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return PredictionResponse(prediction=prediction)
