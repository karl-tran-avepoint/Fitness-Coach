import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiVideoAnalyzer:
    def __init__(self, api_key=None):
        if api_key is None:
            self.client = genai.Client()
        else:
            self.client = genai.Client(api_key=api_key)

    def upload_and_wait(self, file_path):
        myfile = self.client.files.upload(file=file_path)
        file_id = myfile.name
        while True:
            files = self.client.files.list()
            file_state = None
            for f in files:
                if f.name == file_id:
                    file_state = f.state
                    break
            print(f"Current state: {file_state}")
            if file_state == "ACTIVE":
                return myfile
            time.sleep(2)

    def analyze_pose(self, file_path):
        video_file = self.upload_and_wait(file_path)
        prompt = (
            "Analyze the posture in this video at each timestamp. "
            "For each timestamp, return a JSON object with: "
            "timestamp, posture.errors (list of errors), posture.suggestions (list of suggestions). "
            "Format output as: "
            "{'analysis': [{'timestamp': 'MM:SS', 'posture': {'errors': [...], 'suggestions': [...]}}]}"
        )
        response = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[video_file, prompt]
        )
        return response.text

# Example usage:
# analyzer = GeminiVideoAnalyzer()
# result = analyzer.analyze_pose(r"C:\Users\Admin\tuankhaicode\fitness_frontend\backend\videos\output_with_timestamps.mp4")
# print(result)


