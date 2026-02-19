from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    week = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    total_duration = Column(Integer, default=0)  # en minutes
    
    # Relations
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="module", cascade="all, delete-orphan")
