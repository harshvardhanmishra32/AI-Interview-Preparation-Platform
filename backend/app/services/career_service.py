"""Service layer for career path recommendations and learning roadmap generations."""
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.models.user import User
from app.services.ai_service import ai_service
from app.services.analytics_service import AnalyticsService

class CareerService:
    @staticmethod
    def generate_roadmap(db: Session, user_id: int, target_role: str | None = None) -> dict:
        """Combine resume context and mock interview performance data to generate personalized learning roadmap."""
        # 1. Fetch user detail
        user = db.query(User).filter(User.id == user_id).first()
        role = target_role if target_role else (user.target_role if (user and user.target_role) else "Software Engineer")
        
        # 2. Fetch candidate resume details
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        resume_context = {
            "skills": resume.skills if (resume and resume.skills) else ["Communication", "Basic Coding"],
            "projects": resume.projects if (resume and resume.projects) else [],
            "summary": resume.summary if (resume and resume.summary) else "Candidate profile context."
        }
        
        # 3. Retrieve detailed mock interview analytics
        performance_data = AnalyticsService.get_detailed_analytics(db, user_id)
        
        # 4. Generate AI Career Roadmap via Gemini
        roadmap = ai_service.generate_career_roadmap(
            resume_data=resume_context,
            performance_data=performance_data,
            target_role=role
        )
        
        return roadmap
