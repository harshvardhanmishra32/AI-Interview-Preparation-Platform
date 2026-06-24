"""Pytest configuration fixtures setting up database session, client, and authenticated wrappers."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add backend directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.database.base import Base
from app.database.connection import get_db
from main import app

# Test SQLite database setup
from sqlalchemy.pool import StaticPool
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def db_session():
    """Create fresh tables for each test and drop them on completion."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)
        pass

@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient overriding standard DB get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Standard payload template for registration testing."""
    return {
        "name": "Test Candidate",
        "email": "candidate@example.com",
        "password": "Password123!",
        "education": "B.S. Computer Science",
        "target_role": "Software Engineer"
    }

@pytest.fixture
def authenticated_client(client, test_user_data):
    """Pre-register user, request credentials login token, and inject bearer authorization header."""
    # Register user
    client.post("/api/auth/register", json=test_user_data)
    # Login
    response = client.post("/api/auth/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
