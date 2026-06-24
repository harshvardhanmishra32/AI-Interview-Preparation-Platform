"""Service layer for authentication, registration, and user profile management."""
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.analytics import Analytics
from app.schemas.user import UserCreate, UserProfile


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """Register a new user and initialize empty analytics profile."""
        # Check duplicate email
        email = str(user_data.email).lower()
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError("Email is already registered.")

        # Create user record
        db_user = User(
            name=user_data.name,
            email=email,
            password_hash=hash_password(user_data.password),
            education=user_data.education,
            target_role=user_data.target_role,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Initialize analytics record
        db_analytics = Analytics(
            user_id=db_user.id,
            average_score=0.0,
            strongest_topics=[],
            weakest_topics=[],
            total_interviews=0,
        )
        db.add(db_analytics)
        db.commit()

        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        """Authenticate user by email and password verification."""
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Retrieve user by database primary key ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_user_profile(db: Session, user_id: int, profile_data: UserProfile) -> User:
        """Update user identity, education, and target role details."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found.")

        user.name = profile_data.name.strip()
        if profile_data.email:
            next_email = str(profile_data.email).lower()
            duplicate = db.query(User).filter(User.email == next_email, User.id != user_id).first()
            if duplicate:
                raise ValueError("Email is already registered.")
            user.email = next_email
        user.education = profile_data.education
        user.target_role = profile_data.target_role

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user_id: int, current_password: str, new_password: str) -> bool:
        """Verify current password and set a new hashed password. Returns True on success."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found.")
        if not verify_password(current_password, user.password_hash):
            raise ValueError("Current password is incorrect.")

        user.password_hash = hash_password(new_password)
        db.commit()
        return True
