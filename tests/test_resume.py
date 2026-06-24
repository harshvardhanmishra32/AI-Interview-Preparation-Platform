"""Tests for the resume analysis and retrieval endpoints."""
import pytest

def test_upload_resume_unauthenticated(client):
    """Verify that file uploading requires authentication headers."""
    response = client.post("/api/resume/upload-resume", files={"file": ("resume.pdf", b"test", "application/pdf")})
    assert response.status_code == 401

def test_get_resume_no_resume(authenticated_client):
    """Verify response when retrieving resume before uploading any file."""
    response = authenticated_client.get("/api/resume/resume")
    assert response.status_code == 404
    assert "no resume has been uploaded" in response.json()["detail"].lower()
