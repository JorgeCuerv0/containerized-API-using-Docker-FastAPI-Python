# Use Python 3.11-slim image as a base
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

# Set the working directory in the final stage
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy necessary files from the builder stage
COPY --from=builder /app /app

# Set default command for container
CMD ["python3", "src/main.py"]

# Set the healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

