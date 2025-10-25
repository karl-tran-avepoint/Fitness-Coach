from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from google import genai
import time

app = FastAPI()

# Set your Gemini API key here or use environment variable
API_KEY = os.getenv("GOOGLE_API_KEY", "your-api-key-here")
client = genai.Client(api_key=API_KEY)

@app.post("/analyze-video/")
async def analyze_video(file: UploadFile = File(...)):
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only .mp4 videos are supported.")
    
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    try:
        # Upload to Gemini
        myfile = client.files.upload(file=tmp_path)
        file_id = myfile.name
        # Wait for file to become ACTIVE
        while True:
            files = client.files.list()
            file_state = None
            for f in files:
                if f.name == file_id:
                    file_state = f.state
                    break
            if file_state == "ACTIVE":
                break
            time.sleep(2)
        # Send analysis prompt
        prompt = (
            "Analyze the posture in this video at each timestamp. "
            "For each timestamp, return a JSON object with: "
            "timestamp, posture.errors (list of errors), posture.suggestions (list of suggestions). "
            "Format output as: "
            "{'analysis': [{'timestamp': 'MM:SS', 'posture': {'errors': [...], 'suggestions': [...]}}]}"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[myfile, prompt]
        )
        return JSONResponse(content={"result": response.text})
    finally:
        os.remove(tmp_path)
