"""Pydantic schemas for interview sessions, question generation, and answer evaluation."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class QuestionGenerateRequest(BaseModel):
    interview_type: Literal['technical', 'hr', 'behavioral', 'project_based']
    difficulty: Literal['easy', 'medium', 'hard']
    question_count: Literal[5, 10, 20]
    company: str | None = None

class QuestionSchema(BaseModel):
    id: int
    question_text: str
    difficulty: str
    topic: str
    expected_concepts: list[str] | None = None
    
    model_config = ConfigDict(from_attributes=True)

class AnswerSubmitRequest(BaseModel):
    question_id: int
    answer_text: str = Field(..., min_length=1, max_length=8000)

class AnswerEvaluation(BaseModel):
    score: float
    feedback: str
    missing_concepts: list[str] = []
    suggestions: list[str] = []
    ideal_answer: str

class AnswerResponse(BaseModel):
    id: int
    question_id: int
    answer_text: str
    score: float | None = None
    feedback: str | None = None
    missing_concepts: list[str] | None = None
    suggestions: list[str] | None = None
    ideal_answer: str | None = None
    evaluated_at: datetime | None = None
    
    model_config = ConfigDict(from_attributes=True)

class QuestionDetailResponse(BaseModel):
    id: int
    question_text: str
    difficulty: str
    topic: str
    expected_concepts: list[str] | None = None
    answer: AnswerResponse | None = None
    
    model_config = ConfigDict(from_attributes=True)

class InterviewSessionResponse(BaseModel):
    id: int
    company: str | None
    role: str
    interview_type: str
    difficulty: str
    status: str
    created_at: datetime
    questions: list[QuestionDetailResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
