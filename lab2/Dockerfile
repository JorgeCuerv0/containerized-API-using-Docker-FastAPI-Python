# Use the official Python 3.11 slim image as the base for building
FROM python:3.11-slim AS base

# Set the working directory in the container
WORKDIR /app

# Update the package list to ensure we have the latest information on available packages
RUN apt-get update && \  
    # Install necessary system dependencies without unnecessary packages
    apt-get install -y --no-install-recommends \
    curl \                
    build-essential \      
    libffi-dev \           
    ca-certificates \      
    && rm -rf /var/lib/apt/lists/*  

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -  # Download and install Poetry

# Make sure Poetry is in PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry install --no-root  # Install dependencies without installing the package itself

# Copy the source code into the container
COPY . .

# Final Stage: Create a smaller image for running the application
FROM python:3.11-slim AS final

# Set the working directory in the final container
WORKDIR /app

# Copy only the installed packages from the builder stage to the final image
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /root/.local /root/.local

# Install Uvicorn, FastAPI, Joblib, and Scikit-Learn in the final image
RUN pip install --no-cache-dir uvicorn fastapi joblib scikit-learn  # Ensure all necessary packages are installed

# Copy the application code from the base stage to the final image
COPY --from=base /app /app

# Healthcheck to ensure the application is running
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1  # Check if the API is responding

# Run the app using Python with Uvicorn
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
