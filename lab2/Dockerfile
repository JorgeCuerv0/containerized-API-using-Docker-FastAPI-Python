# Base Arguments to leverage across build stages
ARG APP_DIR=/app

#############
# Build (Prepare Environment) image
#############
FROM python:3.11-slim AS build
ARG APP_DIR

# Install necessary system dependencies for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    gfortran \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry directly into the virtual environment
RUN curl -sSL https://install.python-poetry.org | python3 -

# Change the working directory for where our app will live
WORKDIR ${APP_DIR}

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Create a virtual environment for the application
RUN python -m venv --copies ${APP_DIR}/venv

# Activate the virtual environment and install Poetry in it
RUN . ${APP_DIR}/venv/bin/activate && pip install --upgrade pip && pip install poetry

# Install dependencies using Poetry in the virtual environment
RUN . ${APP_DIR}/venv/bin/activate && poetry install --only main

#############
# Deployment image
#############
FROM python:3.11-slim AS run
ARG APP_DIR

# Copy the virtual environment from the build stage
COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv/
ENV PATH="${APP_DIR}/venv/bin:$PATH"

# Set the working directory for the application
WORKDIR ${APP_DIR}

# Copy the application code into the image
COPY . ./

# Healthcheck to ensure the application is running
HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

# Run the application using python with Uvicorn
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
