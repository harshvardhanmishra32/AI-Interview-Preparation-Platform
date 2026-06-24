"""Database connection configuration for SQLite using SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.database.base import Base

# Setup SQLAlchemy SQLite engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    # Importing models here to ensure they are registered on Base
    from app.models.user import User
    from app.models.resume import Resume
    from app.models.interview import InterviewSession, Question, Answer
    from app.models.analytics import Analytics
    
    Base.metadata.create_all(bind=engine)
