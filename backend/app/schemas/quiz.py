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
    questions: List[QuizQuestion]
    passing_score: int
    time_limit: Optional[int] = None

class QuizCreate(BaseModel):
    title: str
    module_id: str
    questions: List[QuizQuestion]
    passing_score: int = 70
    time_limit: Optional[int] = None

class QuizSubmission(BaseModel):
    answers: Dict[str, List[int]]

class QuizResult(BaseModel):
    attempt_id: str
    score: int
    passed: bool
    correct_answers: int
    total_questions: int
    time_taken: int
    answers: Dict[str, bool]
