# Stage 1: Build stage
FROM python:3.11-slim AS build
WORKDIR /app

# Install minimal dependencies
RUN pip install --no-cache-dir \
    fastapi==0.109.2 \
    uvicorn==0.27.1 \
    numpy==1.26.4 \
    scikit-learn==1.5.2 \
    joblib==1.4.2 \
    && find /usr/local -type d -name '__pycache__' -exec rm -r {} + 2>/dev/null || true \
    && find /usr/local -name '*.pyc' -delete

# Copy only necessary files
COPY src/ src/
COPY model_pipeline.pkl .

# Stage 2: Runtime stage
FROM python:3.11-slim
WORKDIR /app

# Copy only necessary files from build stage
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build /app/src/ ./src/
COPY --from=build /app/model_pipeline.pkl .

# Install only curl for healthcheck and clean up in the same layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local -type d -name '__pycache__' -exec rm -r {} + 2>/dev/null || true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/lab/health || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
