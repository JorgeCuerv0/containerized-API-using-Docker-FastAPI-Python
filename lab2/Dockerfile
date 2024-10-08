# Base stage
FROM python:3.11-slim AS base

# Set the working directory
WORKDIR /app

# Install system dependencies without recommended packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Build stage
FROM base AS builder

# Copy only the necessary files for building
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src ./src

# Final stage
FROM base

# Copy installed packages and application code from the builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /app/src ./src

# Expose the port
EXPOSE 8000

# Add a health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
