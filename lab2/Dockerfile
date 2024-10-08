# Step 1: Use the official Python 3.11-slim image as the base for the build
FROM python:3.11-slim AS builder

# Step 2: Set the working directory in the container to /app
WORKDIR /app

# Step 3: Install necessary build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Step 5: Add Poetry to the system PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 6: Copy the dependency files (pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock ./

# Step 7: Install only production dependencies using Poetry
RUN poetry install --only main --no-root

# Step 8: Copy the app's source code
COPY . /app

# Step 9: Install minimal production dependencies
FROM python:3.11-slim

WORKDIR /app

# Step 10: Copy from the builder
COPY --from=builder /app /app

# Step 11: Install necessary production dependencies from Poetry lock
RUN pip install --no-cache-dir fastapi uvicorn joblib scikit-learn

# Step 12: Expose the app port
EXPOSE 8000

# Step 13: Health check
HEALTHCHECK --interval=60s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1

# Step 14: Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
