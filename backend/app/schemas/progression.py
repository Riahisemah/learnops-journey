from pydantic import BaseModel
from typing import List, Optional


class UserProgressionResponse(BaseModel):
    user_id: str
    progression: int
    modules_completed: List[str]        # ✅ List[str] of module IDs e.g. ["devops-basics", "mlops-fundamentals"]
    badges: List[str]
    time_spent: int
    lessons_completed: Optional[int] = 0
    total_lessons: Optional[int] = 0


class ProgressUpdate(BaseModel):
    progression: Optional[int] = None
    modules_completed: Optional[List[str]] = None   # ✅ List[str], was List[int]
    time_spent: Optional[int] = None