from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class LessonType(str, enum.Enum):
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"
    PRACTICE = "practice"

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(String, primary_key=True)
    module_id = Column(String, ForeignKey("modules.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    type = Column(SQLEnum(LessonType), nullable=False)
    duration = Column(String, nullable=False)  # Format: "3:24"
    url = Column(String, nullable=True)
    content = Column(String, nullable=True)
    order = Column(Integer, nullable=False)
    
    # Relations
    module = relationship("Module", back_populates="lessons")
    completions = relationship("LessonCompletion", back_populates="lesson", cascade="all, delete-orphan")
