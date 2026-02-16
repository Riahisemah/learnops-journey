from pydantic import BaseModel
from typing import List, Optional

class LessonResponse(BaseModel):
    id: str
    title: str
    type: str
    duration: str
    completed: bool
    url: Optional[str] = None
    content: Optional[str] = None
    
    class Config:
        from_attributes = True

class ModuleResponse(BaseModel):
    id: str
    title: str
    description: str
    week: int
    order: int
    lessons: List[LessonResponse]
    completion_rate: int
    total_duration: int
    
    class Config:
        from_attributes = True

class ModuleCreate(BaseModel):
    title: str
    description: str
    week: int
    order: int

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    week: Optional[int] = None
    order: Optional[int] = None
