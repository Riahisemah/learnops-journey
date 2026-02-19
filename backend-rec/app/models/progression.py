from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class UserProgression(Base):
    __tablename__ = "user_progressions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    progression = Column(Integer, default=0)  # Pourcentage 0-100
    modules_completed = Column(JSON, default=list)  # [1, 2, 3]
    time_spent = Column(Integer, default=0)  # en secondes
    
    # Relations
    user = relationship("User", back_populates="progression")

class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    badge_name = Column(String, nullable=False)
    
    # Relations
    user = relationship("User", back_populates="badges")

class LessonCompletion(Base):
    __tablename__ = "lesson_completions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    lesson_id = Column(String, ForeignKey("lessons.id", ondelete="CASCADE"))
    completed = Column(Integer, default=1)  # SQLite Boolean (0/1)
    
    # Relations
    lesson = relationship("Lesson", back_populates="completions")
