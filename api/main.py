from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from ultralytics import YOLO
import io
import os
from pathlib import Path
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="YOLOv8 Object Detection API")

# Global variable to store the model
model = None

# Configuration from environment variables
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/yolov8n.pt")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
CONFIDENCE_THRESHOLD_DEFAULT = float(os.getenv("CONFIDENCE_THRESHOLD_DEFAULT", "0.25"))


@app.on_event("startup")
async def startup_event():
    """Load the YOLOv8 model on startup"""
    global model
    try:
        logger.info(f"Loading YOLOv8 model from {MODEL_PATH}...")
        model = YOLO(MODEL_PATH)
        logger.info("Model loaded successfully!")
        
        # Ensure output directory exists
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory ready at {OUTPUT_DIR}")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/detect")
async def detect_objects(
    image: UploadFile = File(...),
    confidence_threshold: float = Form(CONFIDENCE_THRESHOLD_DEFAULT)
):
    """
    Detect objects in an uploaded image using YOLOv8.
    
    Args:
        image: The uploaded image file
        confidence_threshold: Minimum confidence score for detections (default: 0.25)
    
    Returns:
        JSON response with detections and summary
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Validate confidence threshold
        if not 0.0 <= confidence_threshold <= 1.0:
            raise HTTPException(
                status_code=400, 
                detail="confidence_threshold must be between 0.0 and 1.0"
            )
        
        # Read and validate the uploaded image
        try:
            image_bytes = await image.read()
            img = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if img.mode != "RGB":
                img = img.convert("RGB")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(e)}"
            )
        
        # Perform inference
        logger.info(f"Running detection with confidence threshold: {confidence_threshold}")
        results = model(img, conf=confidence_threshold)
        
        # Process results
        detections = []
        class_counts = defaultdict(int)
        
        # Extract detection information
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get bounding box coordinates (xyxy format)
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                
                # Get confidence score
                score = float(box.conf[0])
                
                # Get class label
                class_id = int(box.cls[0])
                label = result.names[class_id]
                
                # Add to detections list
                detections.append({
                    "box": [int(x_min), int(y_min), int(x_max), int(y_max)],
                    "label": label,
                    "score": round(score, 2)
                })
                
                # Update class counts
                class_counts[label] += 1
        
        # Save annotated image
        output_path = os.path.join(OUTPUT_DIR, "last_annotated.jpg")
        
        # Get annotated image from results
        annotated_img = results[0].plot()  # This returns a numpy array with annotations
        
        # Convert numpy array to PIL Image and save
        annotated_pil = Image.fromarray(annotated_img)
        annotated_pil.save(output_path)
        logger.info(f"Annotated image saved to {output_path}")
        
        # Prepare response
        response = {
            "detections": detections,
            "summary": dict(class_counts)
        }
        
        logger.info(f"Detection complete: {len(detections)} objects found")
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "name": "YOLOv8 Object Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/detect": "Object detection (POST)",
        }
    }

