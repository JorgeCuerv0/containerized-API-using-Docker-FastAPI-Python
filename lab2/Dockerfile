# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock ./

# Install project dependencies without dev dependencies
RUN poetry install --no-dev

# Copy the rest of the application code
COPY . .

# Stage 2: Final Image
FROM python:3.11-alpine

WORKDIR /app

# Install runtime dependencies only
RUN apk add --no-cache libffi && \
    apk add --no-cache --virtual .build-deps gcc musl-dev && \
    apk del .build-deps

# Copy necessary files from the builder image
COPY --from=builder /app /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Health check: pings the /health endpoint every 30s
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost:8000/lab/health || exit 1
