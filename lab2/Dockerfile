# Use a multi-stage build to reduce final image size

# Builder stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency files
COPY requirements.txt ./

# Install dependencies with pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Final stage - Smaller runtime image
FROM python:3.11-slim

WORKDIR /app

# Copy necessary files from the builder stage
COPY --from=builder /app /app

# Install Uvicorn separately
RUN pip install --no-cache-dir uvicorn

# Expose the port
EXPOSE 8000

# Add a healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
