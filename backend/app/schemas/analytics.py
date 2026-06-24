"""Pydantic schemas for analytics dashboard and performance tracking."""
from pydantic import BaseModel, ConfigDict

class TopicPerformance(BaseModel):
    topic: str
    average_score: float
    question_count: int

class ScoreTrendEntry(BaseModel):
    date: str
    average_score: float

class RecentSessionEntry(BaseModel):
    id: int
    company: str | None
    role: str
    interview_type: str
    difficulty: str
    created_at: str
    question_count: int
    completed_count: int
    average_score: float | None

class WeeklyProgressEntry(BaseModel):
    week: str
    average_score: float
    interview_count: int

class DashboardResponse(BaseModel):
    total_interviews: int
    average_score: float
    strongest_topics: list[str] = []
    weakest_topics: list[str] = []
    recent_sessions: list[RecentSessionEntry] = []
    score_trend: list[ScoreTrendEntry] = []

class AnalyticsResponse(BaseModel):
    topic_performance: list[TopicPerformance] = []
    weekly_progress: list[WeeklyProgressEntry] = []
    skill_growth: list[dict] = []  # List of dicts describing skill growth per week
