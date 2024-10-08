# Step 1: Build stage - using a full environment with Poetry for dependency management
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies, including curl for downloading Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry (Python dependency manager)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the system PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock for dependency installation
COPY pyproject.toml poetry.lock ./

# Install production dependencies (no dev dependencies)
RUN poetry install --no-dev

# Copy the rest of the application code
COPY . /app

# Step 2: Final image - only including the application with minimal dependencies
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the dependencies and application from the builder stage
COPY --from=builder /app /app

# Install the runtime dependencies directly (FastAPI, Uvicorn, etc.)
RUN pip install fastapi==0.70.0 uvicorn==0.15.0 joblib==1.4.2 scikit-learn==1.5.2

# Expose port 8000
EXPOSE 8000

# Set the default command to start the FastAPI app with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Define a health check for the container, pointing to the /lab/health endpoint
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/lab/health || exit 1
