"""Pydantic schemas for GitHub profile analyzer."""
import re
from pydantic import BaseModel, Field, field_validator

class RepositoryInfo(BaseModel):
    name: str
    description: str | None = None
    language: str | None = None
    stars: int = 0
    forks: int = 0

class GitHubProjectQuestion(BaseModel):
    project_name: str
    question: str
    expected_concepts: list[str] = []

class GitHubAnalysisRequest(BaseModel):
    github_url: str = Field(..., min_length=3, max_length=160)

    @field_validator("github_url")
    @classmethod
    def validate_github_url(cls, value: str) -> str:
        cleaned = value.strip()
        if not re.search(r"^(https?://)?(www\.)?github\.com/[A-Za-z0-9-]+/?$", cleaned):
            raise ValueError("Enter a valid public GitHub profile URL.")
        return cleaned

class GitHubAnalysisResponse(BaseModel):
    username: str
    repositories: list[RepositoryInfo] = []
    languages: dict[str, int] = {}
    total_repos: int = 0
    contribution_summary: str = ""
    project_questions: list[GitHubProjectQuestion] = []
    skill_assessment: list[str] = []
    recommendations: list[str] = []
