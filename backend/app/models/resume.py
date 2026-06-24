"""SQLAlchemy resume database model."""
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Parsed structure stored as JSON
    skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    projects: Mapped[list | None] = mapped_column(JSON, nullable=True)
    certifications: Mapped[list | None] = mapped_column(JSON, nullable=True)
    experience: Mapped[list | None] = mapped_column(JSON, nullable=True)
    education_details: Mapped[list | None] = mapped_column(JSON, nullable=True)
    
    # AI generated analysis fields
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths: Mapped[list | None] = mapped_column(JSON, nullable=True)
    missing_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    suggestions: Mapped[list | None] = mapped_column(JSON, nullable=True)
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship
    user = relationship("User", back_populates="resumes")
