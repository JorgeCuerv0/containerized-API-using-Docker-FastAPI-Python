# Use the slim version of Python 3.11 for the builder stage
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Update package lists and install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"


# Create a virtual environment
RUN python -m venv ./venv

# Copy the Poetry lock file and the pyproject.toml
COPY poetry.lock pyproject.toml ./

# Install the main dependencies (including numpy and scikit-learn) directly in the virtual environment
RUN ./venv/bin/python -m pip install --no-cache-dir poetry \
    && ./venv/bin/poetry install --only main \
    && ./venv/bin/pip install --no-cache-dir uvicorn fastapi joblib numpy scikit-learn \
    && ./venv/bin/pip cache purge

# Second stage: Running the application
FROM python:3.11-slim AS runner
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv

# Set the PATH to include the virtual environment's bin directory
ENV PATH="/app/venv/bin:${PATH}"

# Copy the rest of the application code
COPY . .

# Healthcheck command to ensure the API is up
HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["/app/venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
