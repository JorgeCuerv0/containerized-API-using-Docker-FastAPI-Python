# Builder stage: Use a slim base image and install only what's necessary for building
FROM python:3.11-slim AS builder

WORKDIR /app

# Install necessary system dependencies and clean up afterward
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Final stage: Use a clean slim image
FROM python:3.11-slim

WORKDIR /app

# Copy only what's necessary
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /app /app

# Install FastAPI and Uvicorn, avoiding unnecessary dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Expose the port
EXPOSE 8000

# Add the healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Start the app using the absolute path to uvicorn
CMD ["python3", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
