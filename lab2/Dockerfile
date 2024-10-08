# Use the official Python 3.11 slim image as the base for building
FROM python:3.11-slim AS base

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Make sure Poetry is in PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the source code
COPY . .

# Final Stage: Create a smaller image for running the application
FROM python:3.11-slim AS final

# Set the working directory in the final container
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /root/.local /root/.local

# Copy the application code
COPY --from=base /app /app

# Install all required packages in the final image
RUN pip install --no-cache-dir -e .  # This ensures that all dependencies from pyproject.toml are installed

# Run the app using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
