"""Vercel serverless adapter for the FastAPI backend.

This file keeps the local backend layout unchanged while exposing the FastAPI
ASGI application from Vercel's expected `api/` entrypoint.
"""
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402

