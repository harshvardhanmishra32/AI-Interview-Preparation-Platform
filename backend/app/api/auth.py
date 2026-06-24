"""API endpoints for user authentication, registration, and profile management."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.core.config import settings
from app.database.connection import get_db
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, TokenResponse, UserProfile,
    PasswordChangeRequest, PasswordChangeResponse, RefreshTokenRequest,
)
from app.services.auth_service import AuthService
from app.core.security import create_access_token, decode_access_token
from app.middleware.auth_middleware import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new candidate profile."""
    try:
        user = AuthService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def _parse_login_payload(request: Request) -> UserLogin:
    """Support OAuth2 form login and JSON login without breaking existing clients."""
    content_type = request.headers.get("content-type", "")
    try:
        if "application/json" in content_type:
            payload = await request.json()
            return UserLogin.model_validate(payload)
        form = await request.form()
        return UserLogin(
            email=form.get("username") or form.get("email"),
            password=form.get("password"),
            remember_me=str(form.get("remember_me", "false")).lower() in {"1", "true", "yes", "on"},
        )
    except (ValidationError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Valid email and password are required.",
        )


def _issue_tokens(user: User, remember_me: bool = False) -> dict:
    access_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    if remember_me:
        access_minutes = max(access_minutes, 60 * 24 * 7)
    access_token = create_access_token(
        data={"sub": user.email, "uid": user.id, "token_use": "access"},
        expires_delta=timedelta(minutes=access_minutes),
    )
    refresh_token = create_access_token(
        data={"sub": user.email, "uid": user.id, "token_use": "refresh"},
        expires_delta=timedelta(days=14 if remember_me else 1),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": access_minutes * 60,
        "user": user,
    }


@router.post("/login", response_model=TokenResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    """Authenticate email/password and issue bearer access and refresh tokens."""
    credentials = await _parse_login_payload(request)
    user = AuthService.authenticate_user(db, str(credentials.email), credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _issue_tokens(user, credentials.remember_me)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for a new access token."""
    decoded = decode_access_token(payload.refresh_token)
    if not decoded or decoded.get("token_use") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = decoded.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return _issue_tokens(user, remember_me=False)


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Fetch current user's profile details."""
    return current_user


@router.put("/profile", response_model=UserResponse)
def update_profile(
    profile_data: UserProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's name, education, and target role."""
    try:
        user = AuthService.update_user_profile(db, current_user.id, profile_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/change-password", response_model=PasswordChangeResponse)
def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change password after verifying the current password."""
    try:
        AuthService.change_password(
            db, current_user.id, payload.current_password, payload.new_password
        )
        return PasswordChangeResponse()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
