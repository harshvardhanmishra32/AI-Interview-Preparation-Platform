"""Service layer for parsing, analyzing, and storing candidate resumes with ChromaDB embedding indexing."""
import logging
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.models.user import User
from app.services.ai_service import ai_service
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.chroma_client import add_resume_embeddings

logger = logging.getLogger(__name__)

class ResumeService:
    @staticmethod
    def process_resume(db: Session, user_id: int, file_bytes: bytes) -> Resume:
        """Extract text from PDF, call Gemini, save results to SQLite, and store in ChromaDB."""
        # 1. Parse text from PDF bytes
        resume_text = extract_text_from_pdf(file_bytes)
        
        # 2. Call AI service for structured analysis
        analysis = ai_service.analyze_resume(resume_text)
        
        # Check if user already has a resume
        db_resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        
        if db_resume:
            # Update existing resume
            db_resume.resume_text = resume_text
            db_resume.skills = analysis.get("skills", [])
            db_resume.projects = analysis.get("projects", [])
            db_resume.certifications = analysis.get("certifications", [])
            db_resume.experience = analysis.get("experience", [])
            db_resume.education_details = analysis.get("education", [])
            db_resume.summary = analysis.get("summary", "")
            db_resume.strengths = analysis.get("strengths", [])
            db_resume.missing_skills = analysis.get("missing_skills", [])
            db_resume.suggestions = analysis.get("suggestions", [])
        else:
            # Create new resume
            db_resume = Resume(
                user_id=user_id,
                resume_text=resume_text,
                skills=analysis.get("skills", []),
                projects=analysis.get("projects", []),
                certifications=analysis.get("certifications", []),
                experience=analysis.get("experience", []),
                education_details=analysis.get("education", []),
                summary=analysis.get("summary", ""),
                strengths=analysis.get("strengths", []),
                missing_skills=analysis.get("missing_skills", []),
                suggestions=analysis.get("suggestions", [])
            )
            db.add(db_resume)
            
        db.commit()
        db.refresh(db_resume)
        
        # 3. Add to ChromaDB vector store for semantic retrieval
        # Store user details in metadata for query filtering
        user = db.query(User).filter(User.id == user_id).first()
        metadata = {
            "user_id": user_id,
            "name": user.name if user else "Candidate",
            "target_role": user.target_role if user and user.target_role else "Software Engineer"
        }
        
        try:
            add_resume_embeddings(
                user_id=user_id,
                resume_text=resume_text,
                metadata=metadata
            )
        except Exception as exc:
            logger.warning("Resume vector indexing failed for user %s: %s", user_id, exc)
        
        return db_resume

    @staticmethod
    def get_user_resume(db: Session, user_id: int) -> Resume | None:
        """Fetch the candidate's latest resume analysis record."""
        return db.query(Resume).filter(Resume.user_id == user_id).first()
