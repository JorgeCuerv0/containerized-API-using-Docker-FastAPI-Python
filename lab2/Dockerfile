# Stage 1: Build stage
FROM python:3.11-slim AS build
WORKDIR /app

# Install the necessary dependencies
RUN pip install --no-cache-dir \
    fastapi==0.109.2 \
    uvicorn==0.27.1 \
    numpy==1.26.4 \
    scikit-learn==1.5.2 \
    joblib==1.4.2 \
    && find /usr/local -type d -name '__pycache__' -exec rm -r {} + 2>/dev/null || true \
    && find /usr/local -name '*.pyc' -delete

# Copy the source code and model file
COPY src/ src/
COPY model_pipeline.pkl .

# Stage 2: Runtime stage
FROM python:3.11-slim
WORKDIR /app

# Copy the installed packages and source code from the build stage
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build /app/src/ ./src/
COPY --from=build /app/model_pipeline.pkl .

# Install curl for health checks and clean up
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local -type d -name '__pycache__' -exec rm -r {} + 2>/dev/null || true

# Expose port 8000 for the app
EXPOSE 8000  

# Define a health check to monitor the application
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/lab/health || exit 1

# Run the application using uvicorn
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
