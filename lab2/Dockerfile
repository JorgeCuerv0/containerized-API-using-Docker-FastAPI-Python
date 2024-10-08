# Use the official Python 3.11 slim image
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

# Copy the source code
COPY . .

# Final Stage: Run the application in a smaller image
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Copy the application code
COPY --from=builder /app /app

# Install both FastAPI and Uvicorn
RUN pip install --no-cache-dir fastapi uvicorn

# Expose the port
EXPOSE 8000

# Add the healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
