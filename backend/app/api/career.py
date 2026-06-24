"""API endpoints for generating personalized career roadmaps and recommendation steps."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.career import CareerRoadmapRequest, CareerRoadmapResponse
from app.services.career_service import CareerService

router = APIRouter()

@router.post("/generate-roadmap", response_model=CareerRoadmapResponse)
def generate_roadmap(
    request: CareerRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate custom learning path, recommended certifications, and projects."""
    try:
        roadmap = CareerService.generate_roadmap(db, current_user.id, request.target_role)
        return roadmap
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate career roadmap. Please try again."
        )
