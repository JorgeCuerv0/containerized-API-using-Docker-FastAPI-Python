FROM python:3.11-slim AS builder

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only necessary files for dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy all files
COPY . .

FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy necessary files from builder
COPY --from=builder /app /app

# Entrypoint or command (no explicit uvicorn)
CMD ["python", "-m", "src.main"]  # Assuming your main script is in src/main.py
