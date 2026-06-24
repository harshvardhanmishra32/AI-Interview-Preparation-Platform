"""SQLAlchemy database model for user analytics and performance tracking."""
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Float, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Analytics(Base):
    __tablename__ = "analytics"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    
    average_score: Mapped[float] = mapped_column(Float, default=0.0)
    strongest_topics: Mapped[list | None] = mapped_column(JSON, nullable=True)
    weakest_topics: Mapped[list | None] = mapped_column(JSON, nullable=True)
    total_interviews: Mapped[int] = mapped_column(Integer, default=0)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship
    user = relationship("User", back_populates="analytics")
