"""Tests for registration, login, and user profile management endpoints."""
import pytest

def test_register_user_success(client, test_user_data):
    """Verify standard candidate registration."""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["name"] == test_user_data["name"]
    assert "id" in data

def test_register_duplicate_email(client, test_user_data):
    """Verify that registering with duplicate email raises bad request."""
    # First registration
    client.post("/api/auth/register", json=test_user_data)
    # Second registration
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

def test_login_success(client, test_user_data):
    """Verify successful authentication returns token."""
    # Register first
    client.post("/api/auth/register", json=test_user_data)
    # Login
    response = client.post("/api/auth/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user_data):
    """Verify authentication fails for incorrect password."""
    # Register first
    client.post("/api/auth/register", json=test_user_data)
    # Login with wrong password
    response = client.post("/api/auth/login", data={
        "username": test_user_data["email"],
        "password": "WrongPassword!"
    })
    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()

def test_get_profile_authenticated(authenticated_client, test_user_data):
    """Verify profile retrieval for authenticated credentials client."""
    response = authenticated_client.get("/api/auth/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]

def test_get_profile_unauthenticated(client):
    """Verify unauthenticated profile access returns unauthorized."""
    response = client.get("/api/auth/profile")
    assert response.status_code == 401
