"""SQLAlchemy models for interview sessions, questions, and answers."""
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Text, Float, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    company: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    interview_type: Mapped[str] = mapped_column(String(50), nullable=False)  # technical, hr, behavioral, project_based
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)      # easy, medium, hard
    status: Mapped[str] = mapped_column(String(20), default="in_progress")   # in_progress, completed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    questions = relationship("Question", back_populates="session", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    expected_concepts: Mapped[list | None] = mapped_column(JSON, nullable=True)
    
    # Relationships
    session = relationship("InterviewSession", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False, cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # AI evaluation results
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    missing_concepts: Mapped[list | None] = mapped_column(JSON, nullable=True)
    suggestions: Mapped[list | None] = mapped_column(JSON, nullable=True)
    ideal_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    evaluated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    question = relationship("Question", back_populates="answer")
