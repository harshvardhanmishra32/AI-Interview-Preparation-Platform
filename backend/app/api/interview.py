"""API endpoints for mock interview sessions, question generation, and answer evaluation."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.interview import (
    QuestionGenerateRequest,
    InterviewSessionResponse,
    AnswerSubmitRequest,
    AnswerResponse
)
from app.services.interview_service import InterviewService

router = APIRouter()

@router.post("/generate-questions", response_model=InterviewSessionResponse)
def generate_questions(
    request: QuestionGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start mock interview session and generate questions using Gemini API."""
    try:
        session = InterviewService.create_session(db, current_user.id, request)
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate questions. Please try again."
        )

@router.post("/submit-answer", response_model=AnswerResponse)
def submit_answer(
    request: AnswerSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit candidate response and evaluate using Gemini AI."""
    try:
        answer = InterviewService.submit_answer(
            db=db,
            user_id=current_user.id,
            question_id=request.question_id,
            answer_text=request.answer_text
        )
        return answer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Evaluation failed. Please try again."
        )

@router.get("/history", response_model=list[InterviewSessionResponse])
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve history of all interview sessions conducted by user."""
    return InterviewService.get_user_sessions(db, current_user.id)

@router.get("/interview/{session_id}", response_model=InterviewSessionResponse)
def get_interview(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve details of a specific mock interview session."""
    session = InterviewService.get_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found."
        )
    return session
