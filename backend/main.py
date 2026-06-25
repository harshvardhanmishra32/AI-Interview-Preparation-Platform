"""Main FastAPI entry point file for the AI Interview Preparation Assistant backend."""
from contextlib import asynccontextmanager
from time import monotonic
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.connection import init_db

# Import routers
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.interview import router as interview_router
from app.api.analytics import router as analytics_router
from app.api.github import router as github_router
from app.api.career import router as career_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    # Initialize DB schemas
    init_db()
    
    # Ensure upload directory exists
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    
    yield
    # Shutdown actions (if any)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS middleware — explicit origins required when allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.FRONTEND_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_RATE_LIMIT_BUCKETS: dict[str, list[float]] = {}


@app.middleware("http")
async def security_headers_and_rate_limit(request, call_next):
    """Apply baseline security headers and a small auth abuse guard."""
    if request.url.path in {"/api/auth/login", "/api/auth/register"}:
        now = monotonic()
        client_host = request.client.host if request.client else "unknown"
        key = f"{client_host}:{request.url.path}"
        recent = [ts for ts in _RATE_LIMIT_BUCKETS.get(key, []) if now - ts < 60]
        if len(recent) >= 20:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many attempts. Please wait a minute and try again."},
            )
        recent.append(now)
        _RATE_LIMIT_BUCKETS[key] = recent

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
    return response

# Register routes under /api
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(resume_router, prefix="/api/resume", tags=["Resume"])
app.include_router(interview_router, prefix="/api/interview", tags=["Interview"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(github_router, prefix="/api/github", tags=["GitHub"])
app.include_router(career_router, prefix="/api/career", tags=["Career"])

@app.get("/")
def read_root():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
