import time
from google import genai
from dotenv import load_dotenv
from prompts.prompts import PROMPT_GET_EXERCISE_NAME, PROMPT_ANALYZE_POSE
from prompts.excercise_criterias import CRITERIAS_MAP
from models.schemas import ExerciseNameResponse, GeminiAnalysisResponse, GeminiAnalysisAPIResponse, AnalysisMomentAPIResponse
from video_helper import add_timestamps_to_video, cut_image
import os

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
            model="gemini-2.5-flash",
            contents=[video_file, PROMPT_GET_EXERCISE_NAME],
            config = {
                "response_mime_type": "application/json",
                "response_schema": ExerciseNameResponse
            }
        )
        excercise_name = response.parsed.label
        criteria = CRITERIAS_MAP.get(excercise_name)
        base_name, extension = os.path.splitext(file_path)
        timestamp_video_filepath = f"{base_name}_timestamp{extension}"
        add_timestamps_to_video(file_path, timestamp_video_filepath)
        timestamp_video_file = self.upload_and_wait(timestamp_video_filepath)
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[timestamp_video_file, PROMPT_ANALYZE_POSE.format(criteria=criteria)],
            config = {
                "response_mime_type": "application/json",
                "response_schema": GeminiAnalysisResponse
            }
        )
        
        analysis_response:GeminiAnalysisResponse = response.parsed
        moment_api_response = []
        for moment in analysis_response.analysis:
            base64_img = cut_image(moment.timestamp, file_path)
            if base64_img:
                moment_api_response.append(AnalysisMomentAPIResponse(posture=moment.posture,
                                                                    image_base64=base64_img))
        return GeminiAnalysisAPIResponse(analysis=moment_api_response)


# analyzer = GeminiVideoAnalyzer()

# result = analyzer.analyze_pose(r"C:\Users\Admin\tuankhaicode\fitness_frontend\backend\videos\output_with_timestamps.mp4")
# print(result)


