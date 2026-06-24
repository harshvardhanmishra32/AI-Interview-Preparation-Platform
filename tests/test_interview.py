"""Tests for interview simulator, question generation, and answer submissions."""
import pytest

def test_generate_questions_unauthenticated(client):
    """Verify mock session setup requires credentials."""
    payload = {
        "interview_type": "technical",
        "difficulty": "medium",
        "question_count": 5
    }
    response = client.post("/api/interview/generate-questions", json=payload)
    assert response.status_code == 401

def test_generate_questions_invalid_type(authenticated_client):
    """Verify validation checking blocks invalid options."""
    payload = {
        "interview_type": "invalid_type",
        "difficulty": "medium",
        "question_count": 5
    }
    response = authenticated_client.post("/api/interview/generate-questions", json=payload)
    assert response.status_code == 422  # Pydantic validation error

def test_get_history_empty(authenticated_client):
    """Verify history endpoint returns empty list for new users."""
    response = authenticated_client.get("/api/interview/history")
    assert response.status_code == 200
    assert response.json() == []

def test_submit_answer_invalid_question(authenticated_client):
    """Verify that submitting answers to non-existent question IDs raises errors."""
    payload = {
        "question_id": 9999,
        "answer_text": "Sample candidate answer text."
    }
    response = authenticated_client.post("/api/interview/submit-answer", json=payload)
    assert response.status_code == 400
    assert "question not found" in response.json()["detail"].lower()
