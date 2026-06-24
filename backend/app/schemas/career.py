"""Pydantic schemas for the career roadmap generator."""
from pydantic import BaseModel, Field

class CareerRoadmapRequest(BaseModel):
    target_role: str | None = Field(None, max_length=100)

class LearningPathStep(BaseModel):
    skill: str
    resource: str
    duration: str
    priority: str

class SuggestedProject(BaseModel):
    title: str
    description: str
    skills_practiced: list[str] = []

class CareerPhase(BaseModel):
    phase: str
    duration: str
    goals: list[str] = []
    milestones: list[str] = []

class CareerRoadmapResponse(BaseModel):
    skill_gaps: list[str] = []
    learning_path: list[LearningPathStep] = []
    recommended_certifications: list[str] = []
    suggested_projects: list[SuggestedProject] = []
    timeline: str = ""
    career_roadmap: list[CareerPhase] = []
