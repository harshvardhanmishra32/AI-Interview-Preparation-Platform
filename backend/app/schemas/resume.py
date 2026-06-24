"""Pydantic v2 schemas for resume upload and analysis."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ResumeAnalysis(BaseModel):
    skills: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []
    experience: list[str] = []
    education: list[str] = []
    summary: str = ""
    strengths: list[str] = []
    missing_skills: list[str] = []
    suggestions: list[str] = []

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    skills: list[str] | None = None
    projects: list[str] | None = None
    certifications: list[str] | None = None
    experience: list[str] | None = None
    education_details: list[str] | None = None
    summary: str | None = None
    strengths: list[str] | None = None
    missing_skills: list[str] | None = None
    suggestions: list[str] | None = None
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
