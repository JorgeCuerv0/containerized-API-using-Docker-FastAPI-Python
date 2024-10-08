# Step 1: Use a minimal Python image to reduce the size
FROM python:3.11-slim AS builder

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl gcc g++ && rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Step 5: Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 6: Copy Poetry files to install dependencies
COPY pyproject.toml poetry.lock ./

# Step 7: Install dependencies without dev packages
RUN poetry install --no-dev

# Step 8: Copy the application code
COPY . /app

# Step 9: Exclude unnecessary cache files
RUN rm -rf /root/.cache

# Step 10: Create a lightweight final image
FROM python:3.11-slim

# Step 11: Set the working directory
WORKDIR /app

# Step 12: Copy the dependencies from the builder stage
COPY --from=builder /app /app

# Step 13: Install only essential runtime dependencies (optional, if any additional are needed)
RUN pip install --no-cache-dir fastapi uvicorn

# Step 14: Expose the application port
EXPOSE 8000

# Step 15: Set the default command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Step 16: Add a healthcheck for the container
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1
