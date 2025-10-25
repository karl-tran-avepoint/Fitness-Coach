import base64
import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from call_gemini import GeminiVideoAnalyzer
from models.schemas import GeminiAnalysisAPIResponse


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

analyzer = GeminiVideoAnalyzer()

@app.post("/analyze-video/",
          response_model=GeminiAnalysisAPIResponse)
async def analyze_video(file: UploadFile = File(...)):
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only .mp4 videos are supported.")
    
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        tmp_video_path = tmp.name
    
    try:
        analyze_result = analyzer.analyze_pose(tmp_video_path)
        return analyze_result
        
    finally:
        # Clean up the temporary video file
        os.remove(tmp_video_path)

# To run this file, save it as main.py and run:
# uvicorn main:app --reload