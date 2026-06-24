"""Tests for career roadmap generation and normalization."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

import pytest
from app.services.ai_service import ai_service

def test_generate_roadmap_unauthenticated(client):
    """Verify that generating career roadmaps requires authentication."""
    response = client.post("/api/career/generate-roadmap", json={"target_role": "Backend Engineer"})
    assert response.status_code == 401

def test_normalize_roadmap_standard():
    """Verify normalize_roadmap handles correct standard inputs."""
    data = {
        "skill_gaps": ["React", "CSS"],
        "learning_path": [{
            "skill": "React",
            "resource": "React Docs",
            "duration": "2 weeks",
            "priority": "high"
        }],
        "recommended_certifications": ["AWS Developer"],
        "suggested_projects": [{
            "title": "Portfolio",
            "description": "Create portfolio",
            "skills_practiced": ["HTML", "React"]
        }],
        "timeline": "3 Months",
        "career_roadmap": [{
            "phase": "Phase 1",
            "duration": "1 month",
            "goals": ["Goal 1"],
            "milestones": ["Milestone 1"]
        }]
    }
    
    normalized = ai_service._normalize_roadmap(data)
    
    assert normalized["skill_gaps"] == ["React", "CSS"]
    assert normalized["learning_path"][0]["skill"] == "React"
    assert normalized["learning_path"][0]["priority"] == "High"  # title-cased
    assert normalized["recommended_certifications"] == ["AWS Developer"]
    assert normalized["suggested_projects"][0]["title"] == "Portfolio"
    assert normalized["timeline"] == "3 Months"
    assert normalized["career_roadmap"][0]["phase"] == "Phase 1"

def test_normalize_roadmap_alternative_keys():
    """Verify normalize_roadmap correctly maps alternative keys from LLM outputs."""
    data = {
        "skillGaps": ["TypeScript"],
        "learningPathSteps": [{
            "skill_name": "TypeScript",
            "suggested_resource": "TypeScript Handbook",
            "time": "1 week",
            "priority_level": "medium"
        }],
        "certifications": ["Certified Developer"],
        "projects": [{
            "name": "App",
            "project_description": "Create App",
            "skills": ["TS"]
        }],
        "duration": "1 Month",
        "roadmap": [{
            "name": "Phase 1",
            "time": "2 weeks",
            "focus_goals": ["Goal 1"],
            "tracking_milestones": ["Milestone 1"]
        }]
    }
    
    normalized = ai_service._normalize_roadmap(data)
    
    assert normalized["skill_gaps"] == ["TypeScript"]
    assert normalized["learning_path"][0]["skill"] == "TypeScript"
    assert normalized["learning_path"][0]["resource"] == "TypeScript Handbook"
    assert normalized["learning_path"][0]["duration"] == "1 week"
    assert normalized["learning_path"][0]["priority"] == "Medium"
    assert normalized["recommended_certifications"] == ["Certified Developer"]
    assert normalized["suggested_projects"][0]["title"] == "App"
    assert normalized["suggested_projects"][0]["description"] == "Create App"
    assert normalized["suggested_projects"][0]["skills_practiced"] == ["TS"]
    assert normalized["timeline"] == "1 Month"
    assert normalized["career_roadmap"][0]["phase"] == "Phase 1"
    assert normalized["career_roadmap"][0]["duration"] == "2 weeks"
    assert normalized["career_roadmap"][0]["goals"] == ["Goal 1"]
    assert normalized["career_roadmap"][0]["milestones"] == ["Milestone 1"]

def test_normalize_roadmap_wrapped():
    """Verify normalize_roadmap extracts nested data if wrapped under single key."""
    data = {
        "career_roadmap": {
            "skill_gaps": ["Go"],
            "learning_path": [],
            "recommended_certifications": [],
            "suggested_projects": [],
            "timeline": "1 month",
            "career_roadmap": []
        }
    }
    
    normalized = ai_service._normalize_roadmap(data)
    assert normalized["skill_gaps"] == ["Go"]
    assert normalized["timeline"] == "1 month"
