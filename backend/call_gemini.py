import time
from google import genai
from dotenv import load_dotenv
from prompts.prompts import PROMPT_GET_EXERCISE_NAME, PROMPT_ANALYZE_POSE
from prompts.excercise_criterias import CRITERIAS_MAP
from models.schemas import ExerciseNameResponse, GeminiAnalysisResponse

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
        # Classify exercise
        response = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[video_file, PROMPT_GET_EXERCISE_NAME],
            config = {
                "response_mime_type": "application/json",
                "response_schema": ExerciseNameResponse
            }
        )
        excercise_name = response.parsed.label
        print(excercise_name)
        criteria = CRITERIAS_MAP.get(excercise_name)
        
        response = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[video_file, PROMPT_ANALYZE_POSE.format(criteria=criteria)],
            config = {
                "response_mime_type": "application/json",
                "response_schema": GeminiAnalysisResponse
            }
        )
        analysis_response = response.parsed
        print(analysis_response)
        return response.text


analyzer = GeminiVideoAnalyzer()
result = analyzer.analyze_pose(r"C:\Users\Admin\tuankhaicode\fitness_frontend\backend\videos\output_with_timestamps.mp4")
print(result)


