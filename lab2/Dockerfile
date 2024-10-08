# Step 1: Use the official Python 3.11-slim image as the base for the build
FROM python:3.11-slim AS builder

# Step 2: Set the working directory in the container to /app
WORKDIR /app

# Step 3: Install system dependencies and build essentials
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Step 4: Copy the requirements file and install dependencies
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the app code
COPY . .

# Step 6: Clean up unnecessary build dependencies to reduce image size
RUN apt-get remove -y build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Step 7: Expose port 8000
EXPOSE 8000

# Step 8: Run the application using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Step 9: Healthcheck for the app
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 CMD curl --fail http://localhost:8000/health || exit 1
