import base64
import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

# --- Pydantic Models for Response Structure ---
# Define the JSON structure you want using Pydantic models

class PostureAnalysis(BaseModel):
    errors: List[str]
    suggestions: List[str]

class AnalysisItem(BaseModel):
    image_base64: str
    posture: PostureAnalysis

class AnalysisResponse(BaseModel):
    analysis: List[AnalysisItem]

# --- FastAPI App Initialization ---

app = FastAPI()

# --- Helper Function ---

def encode_image_to_base64(image_path: Path) -> str | None:
    """Reads an image file and returns it as a base64 encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception:
        return None

# --- Endpoint Implementation ---

# Define the base directory for the sample images
# This assumes 'main.py' is in your project's root folder
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "sample_images"


@app.post("/analyze-video/", response_model=AnalysisResponse)
async def analyze_video(file: UploadFile = File(...)):
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only .mp4 videos are supported.")
    
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        tmp_video_path = tmp.name
    
    try:
        # --- Start of Analysis Logic ---
        
        # 1. Find the two sample images from the specified folder
        image_extensions = ['*.jpg', '*.jpeg', '*.png']
        image_files = []
        for ext in image_extensions:
            image_files.extend(IMAGE_DIR.glob(ext))

        if len(image_files) < 2:
            raise HTTPException(
                status_code=500, 
                detail=f"Server error: Could not find 2 images in {IMAGE_DIR}"
            )

        # 2. Encode the first two images to base64
        base64_img_1 = encode_image_to_base64(image_files[0])
        base64_img_2 = encode_image_to_base64(image_files[1])

        if not base64_img_1 or not base64_img_2:
            raise HTTPException(
                status_code=500, 
                detail="Server error: Failed to encode images."
            )

        # 3. Construct the response object using your hardcoded data
        analysis_data = [
            AnalysisItem(
                image_base64=base64_img_1,
                posture=PostureAnalysis(
                    errors=[
                        "Your lower back is rounding at the bottom of the squat.",
                        "Your chest is dropping forward."
                    ],
                    suggestions=[
                        "Brace your core muscles to keep your back straight throughout the entire movement.",
                        "Focus on keeping your chest lifted and proud, as if showing a logo on your shirt to the wall in front of you."
                    ]
                )
            ),
            AnalysisItem(
                image_base64=base64_img_2,
                posture=PostureAnalysis(
                    errors=[
                        "Your torso is leaning too far forward, indicating a need to sit your hips back more.",
                        "Rounding of the lower back is occurring to achieve depth."
                    ],
                    suggestions=[
                        "Initiate the movement by pushing your hips back as if you're about to sit in a chair.",
                        "Squat only to a depth where you can maintain a neutral, straight spine to build strength with proper form."
                    ]
                )
            )
        ]
        
        # 4. Return the response (FastAPI will serialize this to JSON)
        return AnalysisResponse(analysis=analysis_data)
        
        # --- End of Analysis Logic ---

    finally:
        # Clean up the temporary video file
        os.remove(tmp_video_path)

# To run this file, save it as main.py and run:
# uvicorn main:app --reload