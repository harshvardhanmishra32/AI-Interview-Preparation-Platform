"""API endpoints for user performance tracking and dashboard analytics."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.analytics import DashboardResponse, AnalyticsResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve aggregated dashboard metrics, trends, and recent session summary."""
    return AnalyticsService.get_dashboard_data(db, current_user.id)

@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve detailed analysis on topic performance, weekly averages, and skill growth trends."""
    return AnalyticsService.get_detailed_analytics(db, current_user.id)
