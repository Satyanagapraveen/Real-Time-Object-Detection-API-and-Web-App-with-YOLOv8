# YOLOv8 Object Detection System

A containerized web application and REST API for real-time object detection using the YOLOv8 model. This project provides both a FastAPI backend for object detection inference and a Streamlit frontend for easy interaction.

## 🌟 Features

- **Real-time Object Detection**: Uses YOLOv8 model for fast and accurate object detection
- **REST API**: FastAPI-based backend with comprehensive endpoints
- **Web Interface**: User-friendly Streamlit UI for image upload and visualization
- **Containerized**: Fully Dockerized application with docker-compose orchestration
- **Configurable**: Adjustable confidence thresholds for detection
- **Production-Ready**: Health checks, error handling, and proper logging

## 📋 Prerequisites

- Docker Desktop (or Docker + Docker Compose)
- Git
- At least 4GB of free RAM
- Internet connection (for downloading the YOLOv8 model)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Satyanagapraveen/Real-Time-Object-Detection-API-and-Web-App-with-YOLOv8.git
cd "Object Detection YOLOV8"
```

### 2. Download the YOLOv8 Model

**On Linux/Mac:**

```bash
chmod +x scripts/download_model.sh
./scripts/download_model.sh
```

**On Windows (PowerShell):**

```powershell
# Download using PowerShell
New-Item -Path "models" -ItemType Directory -Force
Invoke-WebRequest -Uri "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt" -OutFile "models\yolov8n.pt"
```

**Alternative (using curl on Windows):**

```bash
mkdir -p models
curl -L -o models/yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

### 3. Configure Environment Variables

The `.env` file is already created with default values. You can modify it if needed:

```env
API_PORT=8000
UI_PORT=8501
MODEL_PATH=/app/models/yolov8n.pt
CONFIDENCE_THRESHOLD_DEFAULT=0.25
OUTPUT_DIR=/app/output
```

### 4. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will:

- Build both the API and UI containers
- Start the services
- The API will be available at http://localhost:8000
- The UI will be available at http://localhost:8501

### 5. Access the Application

- **Web UI**: Open your browser and navigate to http://localhost:8501
- **API Documentation**: Visit http://localhost:8000/docs for interactive API documentation
- **API Health Check**: http://localhost:8000/health

## 📖 Usage

### Using the Web Interface

1. Open http://localhost:8501 in your browser
2. Adjust the confidence threshold using the slider (default: 0.25)
3. Upload an image (JPG, JPEG, or PNG)
4. Click "🚀 Detect Objects"
5. View the results including:
   - Number of detected objects
   - Summary by object class
   - Detailed detection list with bounding boxes and confidence scores
   - Download results as JSON

### Using the API Directly

#### Health Check

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "ok"
}
```

#### Object Detection

```bash
curl -X POST "http://localhost:8000/detect" \
  -F "image=@/path/to/your/image.jpg" \
  -F "confidence_threshold=0.25"
```

Response:

```json
{
  "detections": [
    {
      "box": [150, 200, 250, 400],
      "label": "person",
      "score": 0.92
    },
    {
      "box": [300, 150, 450, 250],
      "label": "car",
      "score": 0.88
    }
  ],
  "summary": {
    "person": 1,
    "car": 1
  }
}
```

#### Using Python

```python
import requests

url = "http://localhost:8000/detect"
files = {"image": open("image.jpg", "rb")}
data = {"confidence_threshold": 0.25}

response = requests.post(url, files=files, data=data)
results = response.json()
print(results)
```

## 🏗️ Project Structure

```
/
├── api/                          # FastAPI application
│   ├── main.py                   # API endpoints and logic
│   ├── Dockerfile                # API container definition
│   └── requirements.txt          # API dependencies
├── ui/                           # Streamlit application
│   ├── app.py                    # UI code
│   ├── Dockerfile                # UI container definition
│   └── requirements.txt          # UI dependencies
├── models/                       # YOLOv8 model storage
│   └── yolov8n.pt               # Pre-trained model (download required)
├── scripts/                      # Helper scripts
│   └── download_model.sh        # Model download script
├── output/                       # Processed images
│   └── last_annotated.jpg       # Latest detection result
├── .env                          # Environment variables
├── .env.example                  # Environment template
├── docker-compose.yml            # Service orchestration
└── README.md                     # This file
```

## 🔧 Configuration

### Environment Variables

| Variable                       | Description                           | Default                  |
| ------------------------------ | ------------------------------------- | ------------------------ |
| `API_PORT`                     | API service port                      | `8000`                   |
| `UI_PORT`                      | UI service port                       | `8501`                   |
| `MODEL_PATH`                   | Path to YOLOv8 model inside container | `/app/models/yolov8n.pt` |
| `CONFIDENCE_THRESHOLD_DEFAULT` | Default confidence threshold          | `0.25`                   |
| `OUTPUT_DIR`                   | Output directory for annotated images | `/app/output`            |

### Model Selection

The default model is `yolov8n.pt` (nano), which is lightweight and fast. You can use other YOLOv8 models:

- `yolov8n.pt` - Nano (fastest, least accurate)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (slowest, most accurate)

Update the download URL in `scripts/download_model.sh` and `MODEL_PATH` in `.env`.

## 🐛 Troubleshooting

### API Health Check Failing

**Symptom**: `docker-compose ps` shows API as unhealthy

**Solutions**:

1. Check logs: `docker-compose logs api`
2. Ensure model file exists: `ls -l models/yolov8n.pt`
3. Verify model path in `.env` matches the actual location
4. Increase health check timeout in docker-compose.yml

### Out of Memory Errors

**Solutions**:

1. Use a smaller model (yolov8n.pt instead of yolov8x.pt)
2. Increase Docker memory limit in Docker Desktop settings
3. Process smaller images

### UI Cannot Connect to API

**Solutions**:

1. Ensure API service is healthy: `docker-compose ps`
2. Check API logs: `docker-compose logs api`
3. Verify `API_URL` environment variable in UI service
4. Restart services: `docker-compose restart`

### Model Download Issues

**Solutions**:

1. Check internet connection
2. Try alternative download method (curl vs wget)
3. Download manually from: https://github.com/ultralytics/assets/releases/

## 🧪 Testing

### Test the API Health Endpoint

```bash
curl http://localhost:8000/health
```

### Test Object Detection with a Sample Image

```bash
# Download a test image
curl -o test_image.jpg https://ultralytics.com/images/bus.jpg

# Run detection
curl -X POST "http://localhost:8000/detect" \
  -F "image=@test_image.jpg" \
  -F "confidence_threshold=0.25"
```

### Test Different Confidence Thresholds

```bash
# Low threshold (more detections)
curl -X POST "http://localhost:8000/detect" \
  -F "image=@test_image.jpg" \
  -F "confidence_threshold=0.1"

# High threshold (fewer detections)
curl -X POST "http://localhost:8000/detect" \
  -F "image=@test_image.jpg" \
  -F "confidence_threshold=0.8"
```

## 📊 API Endpoints

### GET /health

Health check endpoint.

**Response**: `200 OK`

```json
{
  "status": "ok"
}
```

### POST /detect

Object detection endpoint.

**Parameters**:

- `image` (file): Image file (JPG, PNG)
- `confidence_threshold` (form field, optional): Float between 0.0 and 1.0 (default: 0.25)

**Response**: `200 OK`

```json
{
  "detections": [
    {
      "box": [x_min, y_min, x_max, y_max],
      "label": "object_class",
      "score": 0.95
    }
  ],
  "summary": {
    "object_class": count
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid image or parameters
- `500 Internal Server Error`: Detection failed
- `503 Service Unavailable`: Model not loaded

## 🛑 Stopping the Application

```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove everything including images
docker-compose down --rmi all -v
```

## 🔄 Development

### Rebuilding After Code Changes

```bash
docker-compose up --build
```

### Running Services Separately

```bash
# API only
docker-compose up api

# UI only
docker-compose up ui
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# API only
docker-compose logs -f api

# UI only
docker-compose logs -f ui
```

## 📝 Core Requirements Checklist

- ✅ Fully containerized with Docker and docker-compose
- ✅ `.env.example` file with all required variables
- ✅ Model download script (not committed to repo)
- ✅ API health check endpoint (`/health`)
- ✅ Object detection endpoint (`/detect`)
- ✅ Confidence threshold filtering
- ✅ Detection summary by class
- ✅ Annotated image output
- ✅ Streamlit web interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request



## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for the object detection model
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Streamlit](https://streamlit.io/) for the web interface

## 📧 Support

For issues and questions:

1. Check the Troubleshooting section
2. Review API documentation at http://localhost:8000/docs
3. Check Docker logs: `docker-compose logs`
4. Verify all prerequisites are met

---

