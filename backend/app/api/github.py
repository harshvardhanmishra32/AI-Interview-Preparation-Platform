"""API endpoints for analyzing GitHub profiles and repositories."""
from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.github import GitHubAnalysisRequest, GitHubAnalysisResponse
from app.services.github_service import GitHubService

router = APIRouter()

@router.post("/analyze-github", response_model=GitHubAnalysisResponse)
def analyze_github(
    request: GitHubAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """Analyze public GitHub profile and generate repository specific questions."""
    try:
        analysis = GitHubService.analyze_profile(request.github_url)
        return analysis
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GitHub profile analysis failed. Please try again."
        )
