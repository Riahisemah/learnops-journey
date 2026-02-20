from pydantic import BaseModel
from typing import List, Dict, Optional


class QuizQuestion(BaseModel):
    id: str
    question: str
    type: str
    options: List[str]
    correct_answers: List[int]
    explanation: Optional[str] = None


class QuizResponse(BaseModel):
    id: str
    title: str
    module_id: str
    questions: List[dict]          # dict not QuizQuestion — correct_answers stripped server-side
    passing_score: int
    time_limit: Optional[int] = None


class QuizCreate(BaseModel):
    title: str
    module_id: str
    questions: List[QuizQuestion]  # includes correct_answers for admin creation
    passing_score: int = 70
    time_limit: Optional[int] = None


class QuizSubmission(BaseModel):
    answers: Dict[str, List[int]]
    time_taken: Optional[int] = 0  # ✅ seconds — added to match QuizResult


class QuizResult(BaseModel):
    attempt_id: str
    score: int
    passed: bool
    correct_answers: int
    total_questions: int
    time_taken: int
    answers: Dict[str, bool]