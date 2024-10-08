# Use the official Python 3.11 slim image as the base for building
FROM python:3.11-slim AS base

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Make sure Poetry is in PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Set environment variable to skip SSL verification
ENV PIP_NO_VERIFY=*

# Install dependencies without installing the root package
RUN poetry install --no-root

# Copy the application source code into the container
COPY . .

# Final Stage: Create a smaller image for running the application
FROM python:3.11-slim AS final

# Set the working directory in the final container
WORKDIR /app

# Copy the installed packages from the base stage
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /root/.local /root/.local

# Install Uvicorn and FastAPI directly in the final image, skipping SSL verification
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org uvicorn fastapi joblib

# Copy the application code from the base stage to the final image
COPY --from=base /app /app

# Run the app using uvicorn from the local bin path
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
