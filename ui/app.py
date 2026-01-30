import streamlit as st
import requests
from PIL import Image
import os
import io
import json

# Configure page
st.set_page_config(
    page_title="YOLOv8 Object Detection",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 YOLOv8 Object Detection")
st.markdown("Upload an image to detect objects using YOLOv8 model")

# Get API URL from environment variable
API_URL = os.getenv("API_URL", "http://api:8000/detect")
API_HEALTH_URL = os.getenv("API_URL", "http://api:8000").replace("/detect", "/health")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# Check API health
try:
    health_response = requests.get(API_HEALTH_URL, timeout=2)
    if health_response.status_code == 200:
        st.sidebar.success("✅ API is online")
    else:
        st.sidebar.error("❌ API is not responding correctly")
except Exception as e:
    st.sidebar.error(f"❌ Cannot connect to API: {str(e)}")

# Confidence threshold slider
confidence = st.sidebar.slider(
    "Confidence Threshold", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.25, 
    step=0.05,
    help="Only show detections with confidence above this threshold"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This application uses YOLOv8 for real-time object detection. "
    "Upload an image and adjust the confidence threshold to see detected objects."
)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

with col2:
    st.subheader("🎯 Detection Results")
    
    if uploaded_file is not None:
        if st.button("🚀 Detect Objects", type="primary", use_container_width=True):
            with st.spinner("🔄 Detecting objects..."):
                try:
                    # Prepare the request
                    uploaded_file.seek(0)  # Reset file pointer
                    files = {"image": ("image.jpg", uploaded_file.getvalue(), "image/jpeg")}
                    data = {"confidence_threshold": confidence}
                    
                    # Make API request
                    response = requests.post(API_URL, files=files, data=data, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        detections = result.get("detections", [])
                        summary = result.get("summary", {})
                        
                        # Display success message
                        st.success(f"✅ Detection complete! Found {len(detections)} objects")
                        
                        # Display summary
                        if summary:
                            st.markdown("#### 📊 Summary")
                            summary_cols = st.columns(min(len(summary), 4))
                            for idx, (label, count) in enumerate(summary.items()):
                                with summary_cols[idx % len(summary_cols)]:
                                    st.metric(label=label.capitalize(), value=count)
                        
                        # Display detailed detections
                        if detections:
                            st.markdown("#### 📋 Detailed Detections")
                            
                            # Create a table view
                            st.markdown("| # | Label | Confidence | Bounding Box |")
                            st.markdown("|---|-------|-----------|--------------|")
                            
                            for idx, detection in enumerate(detections, 1):
                                label = detection["label"]
                                score = detection["score"]
                                box = detection["box"]
                                box_str = f"[{box[0]}, {box[1]}, {box[2]}, {box[3]}]"
                                st.markdown(f"| {idx} | {label} | {score:.2%} | {box_str} |")
                            
                            # Download JSON results
                            st.markdown("---")
                            result_json = json.dumps(result, indent=2)
                            st.download_button(
                                label="📥 Download Results (JSON)",
                                data=result_json,
                                file_name="detection_results.json",
                                mime="application/json"
                            )
                        else:
                            st.info("ℹ️ No objects detected with the current confidence threshold. Try lowering the threshold.")
                        
                        # Note about annotated image
                        st.markdown("---")
                        st.info("💡 The annotated image with bounding boxes has been saved to the output directory.")
                        
                    elif response.status_code == 400:
                        st.error(f"❌ Bad request: {response.json().get('detail', 'Invalid request')}")
                    elif response.status_code == 503:
                        st.error("❌ Model not loaded. Please wait for the API to initialize.")
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. The image might be too large or the server is busy.")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Please ensure the API service is running.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.info("👈 Please upload an image to start detection")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by YOLOv8 & Streamlit | Built with ❤️"
    "</div>",
    unsafe_allow_html=True
)


