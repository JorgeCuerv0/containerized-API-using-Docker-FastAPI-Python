# Stage 1: Builder stage using python:3.11-slim to install dependencies
FROM python:3.11-slim AS builder

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies and curl, then clean up to reduce size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the system PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy the dependency files (pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock ./

# Install only production dependencies using Poetry, no dev dependencies
RUN poetry install --only main --no-dev --no-root

# Copy the rest of the application code
COPY . .

# Remove unnecessary build dependencies after installation to reduce image size
RUN apt-get remove -y build-essential libffi-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Final stage using python:3.11-slim-buster for a minimized image
FROM python:3.11-slim-buster

# Set the working directory in the final image
WORKDIR /app

# Copy the installed dependencies and app code from the builder stage
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Set the necessary environment variables for Poetry
ENV PATH="/root/.local/bin:$PATH"

# Install production dependencies using pip to ensure minimal image size
RUN pip install --no-cache-dir uvicorn joblib scikit-learn

# Expose the app port
EXPOSE 8000

# Health check endpoint for the FastAPI app
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=5 CMD curl --fail http://localhost:8000/health || exit 1

# Command to run the application using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
