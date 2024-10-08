# Stage 1: Build stage with all dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency files and install only production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Clean unnecessary files
RUN find /app -name '__pycache__' -exec rm -rf {} + \
    && find /app -name '*.pyc' -exec rm -rf {} + \
    && rm -rf /root/.cache

# Stage 2: Slim final image
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies and app files from builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /app /app

# Expose the API port
EXPOSE 8000

# Add healthcheck to monitor the API
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Run the application
CMD ["python3", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
