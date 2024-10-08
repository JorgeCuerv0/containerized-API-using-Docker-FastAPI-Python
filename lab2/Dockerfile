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

# Copy only the requirements and necessary files for the build stage
COPY requirements.txt ./
COPY model_pipeline.pkl ./
COPY src/ ./src/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clean up pycache and other unnecessary files
RUN find /app -name '__pycache__' -exec rm -rf {} + && find /app -name '*.pyc' -exec rm -rf {} +

# Final Stage: Run the application in a smaller image
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/
COPY --from=builder /usr/local/bin/fastapi /usr/local/bin/

# Copy the application code from the builder stage
COPY --from=builder /app/model_pipeline.pkl /app/
COPY --from=builder /app/src /app/src

# Expose the port
EXPOSE 8000

# Add the healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Run the app using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
