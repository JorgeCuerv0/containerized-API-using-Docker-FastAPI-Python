# Step 1: Use the official Python 3.11-slim image as the base for the build
FROM python:3.11-slim AS builder

# Step 2: Set the working directory in the container to /app
WORKDIR /app

# Step 3: Install necessary build dependencies and clean up after
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# Step 4: Add Poetry to the system PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 5: Copy the dependency files (pyproject.toml and poetry.lock) separately to use Docker's cache mechanism
COPY pyproject.toml poetry.lock ./

# Step 6: Install only production dependencies using Poetry and disable the virtual environment
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

# Step 7: Copy the app's source code after installing dependencies to improve cache efficiency
COPY . /app

# Step 8: Remove Poetry and other build dependencies to minimize size in the builder stage
RUN apt-get remove --purge -y curl && apt-get autoremove -y && apt-get clean && rm -rf /root/.local

# Step 9: Start a new, final stage with a smaller Python image to reduce image size further
FROM python:3.11-slim

# Step 10: Set the working directory in the final image
WORKDIR /app

# Step 11: Copy the installed dependencies and source code from the builder stage
COPY --from=builder /app /app

# Step 12: Install minimal necessary dependencies using pip in the final stage
RUN pip install --no-cache-dir uvicorn fastapi joblib scikit-learn

# Step 13: Expose the app port
EXPOSE 8000

# Step 14: Health check to ensure the container is running properly
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=5 CMD curl --fail http://localhost:8000/health || exit 1

# Step 15: Set the command to run the application using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
