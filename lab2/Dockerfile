# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install poetry && poetry install --no-dev

# Copy the rest of the application code
COPY . .

# Stage 2: Final Image
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from the builder image
COPY --from=builder /app /app

# Install runtime dependencies
RUN pip install --no-cache-dir fastapi scikit-learn joblib uvicorn

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Health check: pings the /health endpoint every 30s
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost:8000/lab/health || exit 1
