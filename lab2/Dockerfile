# Use the official Python 3.11 slim image as the base for building
FROM python:3.11-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency files and install only production dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code (excluding unnecessary files via .dockerignore)
COPY . .

# Remove cached files and unnecessary pycache files to reduce image size
RUN find /app -name '__pycache__' -exec rm -rf {} + \
    && find /app -name '*.pyc' -exec rm -rf {} + \
    && rm -rf /root/.cache

# Final Stage: Create the actual running image from Python 3.11-slim
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Copy the application code
COPY --from=builder /app /app

# Install FastAPI and Uvicorn
RUN pip install --no-cache-dir fastapi uvicorn

# Expose the port for the API
EXPOSE 8000

# Add the healthcheck for the API
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Run the FastAPI application using uvicorn
CMD ["python3", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
