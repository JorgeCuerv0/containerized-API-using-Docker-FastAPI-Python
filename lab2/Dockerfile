# Use the Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the poetry files
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
