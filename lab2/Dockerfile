# Builder stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies, including curl for Poetry
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock ./

# Install only production dependencies
RUN poetry install --no-dev

COPY . /app

# Final stage - minimal image
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /app /app

# Only install required dependencies, and clean up if necessary
RUN pip install fastapi uvicorn joblib scikit-learn

# Set up healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
