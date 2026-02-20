from pydantic import BaseModel
from typing import List, Optional


# ── Lesson response (used by moduleService & lessonService) ───────────────────

class LessonResponse(BaseModel):
    id: str
    title: str
    type: str
    duration: int                   # ✅ int (minutes) — matches Lesson interface in lessonService.ts
    description: Optional[str] = None
    completed: Optional[bool] = False
    url: Optional[str] = None
    content: Optional[str] = None   # raw JSON string: { theory, practice }

    class Config:
        from_attributes = True


# ── Structured content sub-types (mirrors lesson-content.ts) ─────────────────

class CodeBlock(BaseModel):
    language: str
    code: str


class ContentSection(BaseModel):
    title: str
    content: str
    codeBlocks: Optional[List[CodeBlock]] = []


class LessonContentResponse(BaseModel):
    """
    Matches LessonContent interface in lessonService.ts:
      { moduleId, lessonId, theory: ContentSection, practice: ContentSection }
    """
    moduleId: str
    lessonId: str
    theory: ContentSection
    practice: ContentSection