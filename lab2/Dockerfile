# Use the official Python 3.11 slim image as the base for building
FROM python:3.11-slim AS base

# Set the working directory in the container to /app
WORKDIR /app

# Update package lists and install necessary system dependencies
# - curl: for downloading Poetry
# - build-essential: for compiling packages
# - libffi-dev: required for certain Python packages
# - ca-certificates: to ensure SSL certificates are trusted
# After installation, clean up the package lists to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download and install Poetry, a dependency management tool for Python
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH so we can use it in the next steps
ENV PATH="${PATH}:/root/.local/bin"

# Copy the dependency configuration files to the container
COPY pyproject.toml poetry.lock ./

# Install the project dependencies using Poetry, excluding the root package
RUN poetry install --no-root

# Copy the entire source code into the container
COPY . .

# Start a new stage for the final image
FROM python:3.11-slim AS final

# Set the working directory in the final container to /app
WORKDIR /app

# Copy only the installed packages from the base stage to the final image
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /root/.local /root/.local

# Install Uvicorn (for serving the app), FastAPI (web framework), joblib (for loading models),
# and scikit-learn (for machine learning) in the final image
RUN pip install --no-cache-dir uvicorn fastapi joblib scikit-learn

# Copy the application code from the base stage to the final image
COPY --from=base /app /app

# Healthcheck to ensure the application is running by pinging the root endpoint
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# Run the app using Python with Uvicorn as the ASGI server
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
