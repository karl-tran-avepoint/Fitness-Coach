import time
from google import genai

from dotenv import load_dotenv

load_dotenv()


client = genai.Client()

# Upload your video file
myfile = client.files.upload(file=r"C:\Users\Admin\tuankhaicode\fitness_frontend\backend\videos\output_with_timestamps.mp4")
file_id = myfile.name  # or myfile.id

# Wait for file to become ACTIVE
while True:
    files = client.files.list()
    file_state = None
    for f in files:
        if f.name == file_id:  # or f.id == file_id
            file_state = f.state
            break
    print(f"Current state: {file_state}")
    if file_state == "ACTIVE":
        break
    time.sleep(2)
# Prompt Gemini for structured posture analysis
prompt = (
    "Analyze the posture in this video at each timestamp. "
    "For each timestamp, return a JSON object with: "
    "timestamp, posture.errors (list of errors), posture.suggestions (list of suggestions). "
    "Format output as: "
    "{'analysis': [{'timestamp': 'MM:SS', 'posture': {'errors': [...], 'suggestions': [...]}}]}"
)

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[myfile, prompt]
)

print(response.text)