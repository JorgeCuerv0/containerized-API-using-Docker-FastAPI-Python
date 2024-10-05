# Use an official lightweight Python image
From python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install poetry && poetry install

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with uvicorn
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Health check: pings the /health endpoint every 30s
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost:8000/lab/health || exit 1
