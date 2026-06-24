"""API endpoints for uploading resumes and retrieving analysis reports."""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.config import settings
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_service import ResumeService

router = APIRouter()

@router.post("/upload-resume", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a candidate's resume (PDF format) and generate analysis details."""
    # Verify file type using filename, MIME, size, and PDF signature.
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf") or file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF resumes are supported."
        )
        
    try:
        file_bytes = await file.read()
        if len(file_bytes) > settings.MAX_FILE_SIZE:
            raise ValueError("Resume file is too large. Maximum allowed size is 10MB.")
        if not file_bytes.startswith(b"%PDF"):
            raise ValueError("Invalid PDF file signature. Please upload a valid text-based PDF.")
        db_resume = ResumeService.process_resume(db, current_user.id, file_bytes)
        return db_resume
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the resume. Please try again."
        )

@router.get("/resume", response_model=ResumeResponse)
def get_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve the current user's latest resume analysis details."""
    resume = ResumeService.get_user_resume(db, current_user.id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume has been uploaded yet."
        )
    return resume
