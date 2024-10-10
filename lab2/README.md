# UC Berkeley MIDS DataSci 255 - Lab 2: Data Models and Inference API Project

Welcome to my UC Berkeley MIDS DataSci 255 **Lab 2** project! This project demonstrates how to build and deploy a **containerized API** using **Docker**, **FastAPI**, **Python**, and integrates a **machine learning model** using **scikit-learn** for inference. The project also showcases proper testing using **pytest** and dependency management with **Poetry**.

## Overview

This project serves as an **API (Application Programming Interface)** that allows users to make predictions using a trained **machine learning model** on housing data. The application is containerized, ensuring seamless execution in any environment without worrying about the environment configuration.

## Endpoints Overview

Our API contains several endpoints where clients can interact with the application:

1. **Health Check Endpoint** (`/lab/health`)  
   - **Purpose:** Verifies if the application is running properly.
   - **Method:** `GET`
   - **Response:**  
     ```json
     {
       "time": "2023-09-01T17:56:46.425347"
     }
     ```

2. **Hello Endpoint** (`/lab/hello?name={your_name}`)  
   - **Purpose:** Returns a personalized greeting message when the `name` query parameter is provided.
   - **Method:** `GET`
   - **Example Response:**  
     ```json
     {
       "message": "Hello {your_name}"
     }
     ```
   - **Error Response:** If the `name` parameter is missing, the API returns a 422 Unprocessable Entity:
     ```json
     {
       "detail": [
         {
           "loc": ["query", "name"],
           "msg": "Field required",
           "type": "missing"
         }
       ]
     }
     ```

3. **Prediction Endpoint** (`/lab/predict`)  
   - **Purpose:** Takes in housing-related data and returns a predicted house price using a machine learning model.
   - **Method:** `POST`
   - **Input:**  
     ```json
     {
       "MedInc": 5.0,
       "HouseAge": 25.0,
       "AveRooms": 6.0,
       "AveBedrms": 1.0,
       "Population": 300.0,
       "AveOccup": 2.5,
       "Latitude": 37.7,
       "Longitude": -122.1
     }
     ```
   - **Response:**  
     ```json
     {
       "prediction": 2.500385206899307
     }
     ```
   - **Error Responses:** The API validates input data and returns appropriate error messages for invalid inputs.

4. **Root Endpoint** (`/`)  
   - **Purpose:** The root path returns a 404 Not Found response by design.
   - **Method:** `GET`
   - **Response:**  
     ```json
     {
       "detail": "Not Found"
     }
     ```

5. **Swagger UI Documentation** (`/docs`)  
   - **Purpose:** Provides interactive API documentation where you can test the endpoints directly.
   - **Method:** `GET`
   - **Response:** Swagger UI interface.

6. **OpenAPI JSON Specification** (`/openapi.json`)  
   - **Purpose:** Returns the OpenAPI 3.1 specification for the API in JSON format.
   - **Method:** `GET`
   - **Response:** A JSON object representing the API specification.

---

## Application Instructions

### 1. Building the Application

#### Install Prerequisites

- Ensure you have **Docker** installed on your system. Alternatively, you can use **Poetry** to manage dependencies if you're not running the app inside Docker.

#### Clone the Repository

- Open your terminal and run the following commands:
    ```bash
    git clone https://github.com/UCB-W255/lab-2-data-models-and-inference-JorgeCuerv0.git
    cd lab-2-data-models-and-inference-JorgeCuerv0
    ```

#### Build the Docker Image

- In the terminal, build the Docker image using the following command:
    ```bash
    docker build -t lab2-app .
    ```

---

### 2. Running the Application

#### Run the Docker Container

- Start the application by running the Docker container with the following command:
    ```bash
    docker run -d -p 8000:8000 lab2-app
    ```
- The app will be accessible on port `8000`. You can open your browser and navigate to:
    - [http://localhost:8000/lab/health](http://localhost:8000/lab/health) for the health check.
    - [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

#### Verify the Application

- Check the `/lab/health` endpoint to ensure the app is running properly:
    ```bash
    curl http://localhost:8000/lab/health
    ```

- Make a prediction by calling the `/lab/predict` endpoint:
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/lab/predict' \
      -H 'Content-Type: application/json' \
      -d '{
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveRooms": 6.0,
        "AveBedrms": 1.0,
        "Population": 300.0,
        "AveOccup": 2.5,
        "Latitude": 37.7,
        "Longitude": -122.1
      }'
    ```

---

### 3. Testing the Application

#### Using Poetry (if not using Docker)

- If you are running the app without Docker, you can use **Poetry** for testing:
    ```bash
    poetry install  # Install dependencies
    poetry shell     # Activate the virtual environment
    ```

#### Run the Tests

- Inside the Poetry shell or your virtual environment, run the tests using **pytest**:
    ```bash
    pytest
    ```

- OR, if using Docker, you can run tests inside the Docker container:
    ```bash
    docker exec -it <container_id> pytest
    ```

This will execute the test suite and validate that all endpoints, including `/lab/predict`, are functioning correctly and respond to different input cases.

---

## Troubleshooting

### Why Wasn't My API Able to Run Originally in the Autograder?

Initially, the API did not run successfully in the autograder due to discrepancies between the Pydantic library versions and mismatches in error messages:

- **Pydantic Version Mismatch**: The code was using features from Pydantic V2 (e.g., `@field_validator`), but the autograder environment expected Pydantic V1 behavior. This caused validation errors and incompatibilities.

- **Error Message Differences**: Pydantic V2 introduced changes in error messages and capitalization, leading to assertion failures in tests that expected Pydantic V1-style messages.

- **Solution**: Updated the code to be compatible with Pydantic V2 by ensuring that validators and error messages align with the expected outputs. Adjusted test cases to match the actual error messages produced by Pydantic V2.

---

## Conclusion

By following these steps, you can easily **build**, **run**, and **test** this FastAPI containerized application. It demonstrates how to integrate machine learning models into a FastAPI-based API, containerize it using Docker, and validate the functionality through unit tests.

If you encounter any issues, feel free to reach out or refer to the [FastAPI documentation](https://fastapi.tiangolo.com/) and [Pydantic documentation](https://docs.pydantic.dev/latest/) for additional help.

---
