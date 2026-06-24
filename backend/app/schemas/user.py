"""Pydantic v2 schemas for user management and authentication."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    education: str | None = Field(None, max_length=200)
    target_role: str | None = Field(None, max_length=100)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")
        checks = [
            any(ch.islower() for ch in value),
            any(ch.isupper() for ch in value),
            any(ch.isdigit() for ch in value),
            any(not ch.isalnum() for ch in value),
        ]
        if sum(checks) < 3:
            raise ValueError("Password must include at least three of: uppercase, lowercase, number, symbol.")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    education: str | None
    target_role: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None
    user: UserResponse | None = None


class UserProfile(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr | None = None
    education: str | None = Field(None, max_length=200)
    target_role: str | None = Field(None, max_length=100)

    @field_validator("name")
    @classmethod
    def clean_profile_name(cls, value: str) -> str:
        return value.strip()


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_new_password_strength(cls, value: str) -> str:
        return UserCreate.validate_password_strength(value)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=20)


class PasswordChangeResponse(BaseModel):
    message: str = "Password updated successfully."
