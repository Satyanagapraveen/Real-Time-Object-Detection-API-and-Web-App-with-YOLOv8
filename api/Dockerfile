# Use Python image with pre-installed ML libs for faster builds
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in steps to avoid hash errors
RUN pip install --upgrade pip

# Install core dependencies first
RUN pip install fastapi==0.104.1 uvicorn==0.24.0 python-multipart==0.0.6 pillow==10.1.0

# Install PyTorch CPU version (smaller and faster)
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install ultralytics and opencv
RUN pip install ultralytics opencv-python-headless

# Copy application code
COPY main.py .

# Create models and output directories
RUN mkdir -p /app/models /app/output

# Expose port
EXPOSE 8000

# Set environment variables
ENV MODEL_PATH=/app/models/yolov8n.pt
ENV OUTPUT_DIR=/app/output
ENV CONFIDENCE_THRESHOLD_DEFAULT=0.25

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
