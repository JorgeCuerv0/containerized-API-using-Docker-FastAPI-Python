# Step 1: Use the official Python 3.11-slim image as the base for the build
FROM python:3.11-slim AS builder

# Step 2: Set the working directory in the container to /app
WORKDIR /app

# Step 3: Install system dependencies, including curl for downloading Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry, a tool to manage Python dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -

# Step 5: Add Poetry to the system PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 6: Copy the pyproject.toml and poetry.lock files to install dependencies
COPY pyproject.toml poetry.lock ./

# Step 7: Install only production dependencies (no dev dependencies) using Poetry
RUN poetry install --no-dev
COPY . /app

# Step 8: Debugging step - output installed packages after installation
RUN pip freeze > /app/installed_packages.txt

# Step 9: Start a new, final stage using a smaller Python image to reduce image size
FROM python:3.11-slim

# Step 10: Set the working directory to /app
WORKDIR /app

# Step 11: Copy the installed dependencies and app files from the builder stage
COPY --from=builder /app /app

# Step 12: Install FastAPI and Uvicorn explicitly in this stage
RUN pip install fastapi uvicorn

# Step 13: Expose port 8000, which will be used by FastAPI/Uvicorn
EXPOSE 8000

# Step 14: Set the default command to start the FastAPI app using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Step 15: Define a health check for the container, pointing to the /lab/health endpoint
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/lab/health || exit 1
