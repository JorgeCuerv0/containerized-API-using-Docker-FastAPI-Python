# Import necessary libraries and modules
from pydantic import BaseModel, ConfigDict  # BaseModel for defining input and output data models, ConfigDict for additional model configuration
from fastapi import FastAPI  # FastAPI class to create an instance of the API
from fastapi.responses import JSONResponse  # JSONResponse for custom responses
from datetime import datetime  # To work with date and time in health check or other endpoints
import joblib  # To load the machine learning model that has been saved using joblib
import numpy as np  # NumPy is used to create arrays that can be passed to the model for prediction

# Create a FastAPI instance (the main app)
app = FastAPI()

# Load the pre-trained machine learning model using joblib
# model_pipeline.pkl should be a pickled version of a trained model (for example, a Scikit-learn pipeline)
model = joblib.load("model_pipeline.pkl")

# Define the input model using Pydantic, which ensures that the input data adheres to certain rules.
# HousingInput defines the expected input fields and their types, which map directly to the input features expected by the ML model.
class HousingInput(BaseModel):
    MedInc: float  # Median income in a given block group
    HouseAge: float  # Median age of houses in the block group
    AveRooms: float  # Average number of rooms per household
    AveBedrms: float  # Average number of bedrooms per household
    Population: float  # Population of the block group
    AveOccup: float  # Average household size (occupants per household)
    Latitude: float  # Latitude of the block group
    Longitude: float  # Longitude of the block group

    # Pydantic's model config to ensure no additional fields are passed that are not defined in the class (extra fields will raise an error).
    model_config = ConfigDict(extra="forbid")

# Define the output model, which specifies what the API will return.
# In this case, it returns the prediction made by the machine learning model.
class HousingOutput(BaseModel):
    prediction: float  # This field will contain the predicted value (e.g., housing price)

# Define an endpoint that listens for POST requests at /predict.
# The input data should conform to the HousingInput model, and the response will be structured using the HousingOutput model.
@app.post("/predict", response_model=HousingOutput)
async def predict(input_data: HousingInput):
    # Convert the input data from the HousingInput model into a NumPy array.
    # This array will be passed to the machine learning model for prediction.
    input_array = np.array([[
        input_data.MedInc,       # Median income
        input_data.HouseAge,     # House age
        input_data.AveRooms,     # Average rooms
        input_data.AveBedrms,    # Average bedrooms
        input_data.Population,   # Population
        input_data.AveOccup,     # Average occupancy
        input_data.Latitude,     # Latitude
        input_data.Longitude     # Longitude
    ]])

    # Perform the prediction using the loaded machine learning model.
    # The model expects the input to be a 2D array, hence we pass a list of lists.
    prediction = model.predict(input_array)

    # Return the prediction as an instance of the HousingOutput model.
    # The prediction is rounded and placed inside the HousingOutput model for a clean and structured response.
    return HousingOutput(prediction=prediction[0])  # prediction[0] gets the first (and only) element in the prediction array
