FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy the project files and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY . .

FROM python:3.11-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy necessary files from builder
COPY --from=builder /app /app

# Run the API server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
