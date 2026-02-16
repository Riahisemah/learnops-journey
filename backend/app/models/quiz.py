from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import uuid

class QuestionType(str, enum.Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    BOOLEAN = "boolean"

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    module_id = Column(String, ForeignKey("modules.id", ondelete="CASCADE"))
    passing_score = Column(Integer, default=70)
    time_limit = Column(Integer, nullable=True)  # en secondes
    
    # Questions stockées en JSON
    questions = Column(JSON, nullable=False)
    # Format: [{"id": "q1", "question": "...", "type": "single", "options": [...], "correct_answers": [0], "explanation": "..."}]
    
    # Relations
    module = relationship("Module", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, ForeignKey("quizzes.id", ondelete="CASCADE"))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=False)
    passed = Column(Integer, nullable=False)  # SQLite uses Integer for Boolean (0/1)
    correct_answers = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    time_taken = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=False)  # {"q1": true, "q2": false}
    
    # Relations
    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")
