# Stage 1: Build stage
# We're using the official slim Python 3.11 image as the base image for building the application.
FROM python:3.11-slim AS builder

# Set the working directory in the container to /app.
# This is where all of our application files and dependencies will be placed.
WORKDIR /app

# Update the package lists for apt (the package manager for Debian-based distributions) 
# and install essential build tools like curl, build-essential, and libffi-dev for compiling dependencies.
# `libffi-dev` is required for cryptographic packages.
RUN apt-get update \
    && apt-get install -y \
        curl \                   
        build-essential \         
        libffi-dev \              
    && rm -rf /var/lib/apt/lists/*  

# Install Poetry, a modern Python packaging and dependency management tool.
# We're downloading Poetry using curl and then executing the installation script with Python3.
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry’s installation directory to the PATH environment variable
# so that we can access the `poetry` command globally within the container.
ENV PATH="/root/.local/bin:${PATH}"

# Copy the dependency files (pyproject.toml and poetry.lock) into the /app directory.
# These files define the dependencies and project configuration for Poetry.
COPY poetry.lock pyproject.toml ./

# Use Poetry to install only the main dependencies (exclude dev dependencies).
# We also skip installing the project itself by using --no-root.
# The --no-interaction and --no-ansi flags ensure that the process is automated and quiet.
# After installing the dependencies, we clear the Poetry cache to reduce the image size.
RUN poetry install --only main --no-dev --no-interaction --no-ansi --no-root \
    && poetry cache clear --all --no-interaction \  
    && rm -rf /root/.cache/pypoetry  # Remove the cache to minimize image size.

# Stage 2: Final runtime stage
# We're using another lightweight Python 3.11 slim image as the base for running the application.
FROM python:3.11-slim AS runner

# Set the working directory for the final image to /app.
# This is where the application code and dependencies will reside.
WORKDIR /app

# Copy the installed dependencies from the build stage (builder) into the final image.
# We only copy the necessary dependencies from the build stage to avoid copying extra build tools.
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Copy all the application code from the host machine into the /app directory in the container.
# This includes the source code and any necessary files (like models, configurations, etc.).
COPY . .

# Install only curl for the health check, without any additional recommended packages to minimize image size.
# After installation, clean up unnecessary files from apt to further reduce the size of the final image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \  
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size.

# Define a health check to monitor the application’s health by sending HTTP requests to the /health endpoint.
# The health check runs every 30 seconds, with a timeout of 3 seconds, and it retries 3 times if it fails.
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

# Define the command to run the application when the container starts.
# We're using `uvicorn`, an ASGI server, to run our FastAPI application.
# It listens on all network interfaces (0.0.0.0) and uses port 8000.
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
