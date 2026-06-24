"""Tests for analytics aggregates and progress tracker endpoints."""
import pytest

def test_get_dashboard_unauthenticated(client):
    """Verify dashboard endpoint access is restricted."""
    response = client.get("/api/analytics/dashboard")
    assert response.status_code == 401

def test_get_dashboard_authenticated(authenticated_client):
    """Verify dashboard data format structure for authenticated users."""
    response = authenticated_client.get("/api/analytics/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_interviews" in data
    assert "average_score" in data
    assert data["total_interviews"] == 0
    assert data["average_score"] == 0.0

def test_get_analytics_unauthenticated(client):
    """Verify detailed analytics endpoint access is restricted."""
    response = client.get("/api/analytics/analytics")
    assert response.status_code == 401

def test_get_analytics_authenticated(authenticated_client):
    """Verify detailed analytics data format structure for authenticated users."""
    response = authenticated_client.get("/api/analytics/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "topic_performance" in data
    assert "weekly_progress" in data
    assert "skill_growth" in data
