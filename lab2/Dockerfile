# Step 1: Use the official Python 3.11-slim image as the base for the build
FROM python:3.11-slim AS builder

# Step 2: Set the working directory in the container to /app
WORKDIR /app

# Step 3: Install system dependencies and pip, and clean up afterwards
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Step 5: Add Poetry to the system PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 6: Copy the dependency files (pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock ./

# Step 7: Install only production dependencies using Poetry
RUN poetry install --no-dev --no-root

# Step 8: Copy the rest of the app's source code
COPY . /app

# Step 9: Start a new, final stage with a smaller Python image to reduce image size
FROM python:3.11-slim

# Step 10: Set the working directory in the final image
WORKDIR /app

# Step 11: Copy the installed dependencies and source code from the builder stage
COPY --from=builder /app /app

# Step 12: Install the minimal necessary production dependencies
RUN pip install --no-cache-dir fastapi uvicorn joblib scikit-learn

# Step 13: Expose port 8000
EXPOSE 8000

# Step 14: Set the default command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Step 15: Health check to ensure the container is running properly
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1
