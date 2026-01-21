FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for face_recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache layer)
COPY requirements.txt .

# Install Python dependencies with cache mount
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY packages/ ./packages/

# Create storage directory
RUN mkdir -p /app/storage

# Run worker
CMD ["python", "-m", "src.worker"]
