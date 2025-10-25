from google import genai

from dotenv import load_dotenv

load_dotenv()


client = genai.Client()

# Upload your video file
myfile = client.files.upload(file=r"C:\Users\Admin\tuankhaicode\fitness-coach\backend\videos\output_with_timestamps.mp4")

# Prompt Gemini for structured posture analysis
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

print(response.text)