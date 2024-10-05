# UC Berkeley MIDS DataSci 255 - Lab 2: Data Models and Inference API Project

Welcome to my UC Berkeley MIDS DataSci 255 **Lab 2** project! This project demonstrates how to build and deploy a **containerized API** using **Docker**, **FastAPI**, **Python**, **Poetry**, and integrates a **machine learning model** using **scikit-learn** for inference.

## What is this project?

This project serves as an **API (Application Programming Interface)** that allows users to make predictions using a trained **machine learning model**. The application is containerized, meaning the entire application and its dependencies are bundled together to ensure seamless execution in any environment. You can deploy and run this project anywhere without worrying about the environment configuration.

## Endpoints Overview

Our API contains several endpoints where clients can interact with the application:

1. **Health Check Endpoint** (`/health`)  
   - **Purpose:** Verifies if the application is running properly.
   - **Method:** `GET`
   - **Response:**  
     ```json
     {
       "time": "2023-09-01T17:56:46.425347"
     }
     ```

2. **Hello Endpoint** (`/hello?name={your_name}`)  
   - **Purpose:** Returns a personalized greeting message when the correct query parameter is passed (`name`).
   - **Method:** `GET`
   - **Example Response:**  
     ```json
     {
       "message": "Hello {your_name}!"
     }
     ```
   - **Error Response:** If the `name` parameter is missing or empty, the API returns a 400 Bad Request:
     ```json
     {
       "detail": "Name is required"
     }
     ```

3. **Prediction Endpoint** (`/predict`)  
   - **Purpose:** Takes in housing-related data (longitude, latitude, median income, etc.) and returns a predicted house price using a machine learning model.
   - **Method:** `POST`
   - **Input:**  
     ```json
     {
       "longitude": -122.1,
       "latitude": 37.7,
       "MedInc": 5.0,
       "HouseAge": 25.0,
       "AveBedrms": 1.0,
       "AveRooms": 6.0,
       "population": 300.0,
       "AveOccup": 2.5
     }
     ```
   - **Response:**  
     ```json
     {
       "prediction": 2.500385206899307
     }
     ```

4. **Root Endpoint** (`/`)  
   - **Purpose:** The main page of our application.
   - **Method:** `GET`
   - **Response:** `404 Not Found` (by design)

5. **Swagger UI Documentation** (`/docs`)  
   - **Purpose:** Provides interactive API documentation where you can test the endpoints directly.
   - **Method:** `GET`
   - **Response:** Swagger UI interface

6. **OpenAPI JSON Specification** (`/openapi.json`)  
   - **Purpose:** Returns the OpenAPI 3.1 specification for the API in JSON format.
   - **Method:** `GET`
   - **Response:** A JSON object representing the API spec

---

## Application Instructions

### 1. Building the Application

#### Install Prerequisites
- Ensure you have **Docker** installed on your system. Alternatively, you can use **Poetry** to manage dependencies if you're not running the app inside Docker.

#### Clone the Repository
- Open your terminal and run the following commands:
    ```bash
    git clone https://github.com/UCB-W255/lab-2-data-models-and-inference-JorgeCuerv0
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
    - [http://0.0.0.0:8000/health](http://0.0.0.0:8000/health) for the health check.
    - [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) for interactive API documentation.

#### Verify the Application

Check the `/health` endpoint to ensure the app is running properly:
- Run in your terminal:
    ```bash
    curl http://0.0.0.0:8000/health
    ```

Make a prediction by calling the `/predict` endpoint:
- Run in your terminal:
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/predict' \
      -H 'Content-Type: application/json' \
      -d '{
        "longitude": -122.1,
        "latitude": 37.7,
        "MedInc": 5.0,
        "HouseAge": 25.0,
        "AveBedrms": 1.0,
        "AveRooms": 6.0,
        "population": 300.0,
        "AveOccup": 2.5
      }'
    ```

---

### 3. Testing the Application

#### Activate the Poetry Shell (if not using Docker)
- If you are running the app without Docker, you can use **Poetry** for testing:
    ```bash
    poetry shell
    ```

#### Run the Tests
- Inside the Poetry shell, run the tests using **pytest**:
    ```bash
    poetry run pytest
    ```

OR, if using Docker:
- Use the following command to run tests in Docker:
    ```bash
    docker exec -it <container_id> poetry run pytest
    ```

This will execute the test suite and validate that all endpoints, including `/predict`, are functioning correctly and respond to different input cases.

---

## Conclusion

By following these steps, you can easily **build**, **run**, and **test** this FastAPI containerized application. It demonstrates how to integrate machine learning models into a FastAPI-based API, containerize it using Docker, and validate the functionality through unit tests. If you encounter any issues, feel free to reach out or refer to the [FastAPI documentation](https://fastapi.tiangolo.com/) for additional help.
