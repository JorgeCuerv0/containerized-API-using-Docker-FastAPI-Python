# Step 1: Use python:3.11-slim as the base for building and running the application
FROM python:3.11-slim AS builder

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Install necessary build dependencies
RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Step 5: Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 6: Copy the dependency files (pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock ./

# Step 7: Install dependencies for the app
RUN poetry install --only main --no-root

# Step 8: Copy the application source code
COPY . /app

# Final Stage: Build the final image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the dependencies and application from the builder stage
COPY --from=builder /app /app
COPY --from=builder /usr/local /usr/local

# Install the production dependencies
RUN pip install --no-cache-dir uvicorn fastapi joblib scikit-learn

# Expose the application port
EXPOSE 8000

# Add a health check that polls the /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

# Command to run the application using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
