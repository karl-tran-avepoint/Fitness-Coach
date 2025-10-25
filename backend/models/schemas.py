from pydantic import BaseModel
from typing import List, Literal

class ExerciseNameResponse(BaseModel):
    label: Literal["squat", "push_up", "unknown"]

class Posture(BaseModel):
    errors: List[str]
    suggestions: List[str]

class AnalysisMoment(BaseModel):
    timestamp: str
    posture: Posture

class GeminiAnalysisResponse(BaseModel):
    analysis: List[AnalysisMoment]
    
