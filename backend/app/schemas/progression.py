from pydantic import BaseModel
from typing import List

class UserProgressionResponse(BaseModel):
    user_id: str
    progression: int
    modules_completed: List[int]
    badges: List[str]
    time_spent: int

class ProgressUpdate(BaseModel):
    progression: int
    modules_completed: List[int]
    time_spent: int
