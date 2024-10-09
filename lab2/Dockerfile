# Stage 1 - Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install required build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy poetry files to install dependencies
COPY poetry.lock pyproject.toml ./

# Create virtual environment and install dependencies
RUN python -m venv venv \
    && . /app/venv/bin/activate \
    && poetry install --only main

# Stage 2 - Final image
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv

# Set the PATH to use the venv
ENV PATH="/app/venv/bin:$PATH"

# Copy your source code
COPY . .

# Define command to run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
