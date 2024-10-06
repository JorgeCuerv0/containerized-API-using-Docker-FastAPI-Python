# Use Python 3.11-slim as the base image
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Install system dependencies including curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock ./

# Install the dependencies using Poetry without dev dependencies
RUN poetry install --no-dev

# Copy all files from current context
COPY . .

# Final stage (build from here to reduce image size)
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy necessary files from the builder stage
COPY --from=builder /app /app

# Install Uvicorn explicitly in the final image
RUN pip install uvicorn

# Expose the port FastAPI will run on
EXPOSE 8000

# Set default command to start Uvicorn and run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Set the healthcheck (ensure it points to the correct health endpoint)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/lab/health || exit 1
