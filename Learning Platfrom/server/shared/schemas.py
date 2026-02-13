from typing import List, Optional
from pydantic import BaseModel

# --- Course Generation Schemas ---

class CourseRequest(BaseModel):
    topic: str
    grade_level: str
    framework: Optional[str] = "General"  # e.g., "CBSE", "IGCSE", "General"

class Chapter(BaseModel):
    chapter_number: int
    title: str
    description: str

class CourseRoadmap(BaseModel):
    topic: str
    chapters: List[Chapter]

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int  # Index of the correct option

class ChapterContent(BaseModel):
    chapter_title: str
    content_markdown: str
    quiz: List[QuizQuestion]

class ChapterRequest(BaseModel):
    chapter: Chapter
    topic: str
    grade_level: str

# --- Proctoring Schemas ---

class ProctorStatus(BaseModel):
    user_id: str
    attention_score: float  # 0.0 to 1.0
    is_looking_away: bool
    fraud_detected: bool
    timestamp: float
