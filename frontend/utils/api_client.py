"""HTTP API client library for communicating with the FastAPI backend."""
import streamlit as st
import requests
from requests.exceptions import Timeout, ConnectionError, JSONDecodeError

# Default timeout for all API requests (seconds)
_TIMEOUT = 15


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url

    def _get_headers(self) -> dict:
        """Construct authentication headers dynamically from session state."""
        headers = {}
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _safe_json(self, response: requests.Response) -> dict:
        """Safely parse JSON from response, returning empty dict on failure."""
        try:
            return response.json()
        except (JSONDecodeError, ValueError):
            return {}

    def _handle_error(self, response: requests.Response, fallback: str) -> dict:
        """Extract a user-friendly error message from a failed response."""
        body = self._safe_json(response)
        detail = body.get("detail", fallback)
        if isinstance(detail, list):
            detail = detail[0].get("msg", fallback) if detail and isinstance(detail[0], dict) else fallback
        if response.status_code == 401:
            detail = "Session expired. Please log in again."
        elif response.status_code == 429:
            detail = "Too many requests. Please wait a moment and try again."
        elif response.status_code >= 500:
            detail = "Server error. Please try again later."
        return {"success": False, "error": detail}

    # ─── Auth ──────────────────────────────────────────────────────────

    def register(self, name, email, password, education, target_role) -> dict:
        """Register a new candidate user profile."""
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={"name": name, "email": email, "password": password,
                      "education": education, "target_role": target_role},
                timeout=_TIMEOUT,
            )
            if response.status_code == 201:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Registration failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Cannot reach the server. Is the backend running?"}

    def login(self, email, password, remember_me: bool = False) -> dict:
        """Authenticate user credentials and fetch access token."""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password, "remember_me": remember_me},
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Invalid email or password.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Cannot reach the server. Is the backend running?"}

    def get_profile(self) -> dict:
        """Fetch user profile metadata."""
        try:
            response = requests.get(
                f"{self.base_url}/auth/profile",
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Failed to load profile.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout fetching profile."}

    def update_profile(self, name, education, target_role, email=None) -> dict:
        """Update candidate target role and education details."""
        payload = {"name": name, "education": education, "target_role": target_role}
        if email:
            payload["email"] = email
        try:
            response = requests.put(
                f"{self.base_url}/auth/profile",
                json=payload,
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Profile update failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout updating profile."}

    def change_password(self, current_password: str, new_password: str) -> dict:
        """Change the currently logged-in user's password."""
        try:
            response = requests.post(
                f"{self.base_url}/auth/change-password",
                json={"current_password": current_password, "new_password": new_password},
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Password change failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout changing password."}

    # ─── Resume ────────────────────────────────────────────────────────

    def upload_resume(self, file_bytes, filename) -> dict:
        """Upload a PDF resume file for extraction and analysis."""
        try:
            response = requests.post(
                f"{self.base_url}/resume/upload-resume",
                files={"file": (filename, file_bytes, "application/pdf")},
                headers=self._get_headers(),
                timeout=60,  # Resume processing can take longer
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Resume upload failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Upload timed out. Please try again."}

    def get_resume(self) -> dict:
        """Retrieve latest parsed resume analysis details."""
        try:
            response = requests.get(
                f"{self.base_url}/resume/resume",
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "No resume found.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout fetching resume."}

    # ─── Interview ─────────────────────────────────────────────────────

    def generate_questions(self, interview_type, difficulty, question_count, company=None) -> dict:
        """Request new mock interview session question set."""
        try:
            response = requests.post(
                f"{self.base_url}/interview/generate-questions",
                json={"interview_type": interview_type, "difficulty": difficulty,
                      "question_count": question_count, "company": company},
                headers=self._get_headers(),
                timeout=45,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Question generation failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Request timed out generating questions."}

    def submit_answer(self, question_id, answer_text) -> dict:
        """Submit candidate response for AI evaluation grading."""
        try:
            response = requests.post(
                f"{self.base_url}/interview/submit-answer",
                json={"question_id": question_id, "answer_text": answer_text},
                headers=self._get_headers(),
                timeout=45,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Answer submission failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Request timed out submitting answer."}

    def get_history(self) -> dict:
        """Fetch list of user's past mock interview sessions."""
        try:
            response = requests.get(
                f"{self.base_url}/interview/history",
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Failed to fetch interview history.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout fetching history."}

    def get_interview(self, session_id) -> dict:
        """Fetch full details of a specific past mock interview session."""
        try:
            response = requests.get(
                f"{self.base_url}/interview/interview/{session_id}",
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Failed to load session details.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout loading session."}

    # ─── Analytics ─────────────────────────────────────────────────────

    def get_dashboard(self) -> dict:
        """Retrieve aggregated user dashboard metrics."""
        try:
            response = requests.get(
                f"{self.base_url}/analytics/dashboard",
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Failed to fetch dashboard data.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout loading dashboard."}

    def get_analytics(self) -> dict:
        """Retrieve detailed topic performance and growth statistics."""
        try:
            response = requests.get(
                f"{self.base_url}/analytics/analytics",
                headers=self._get_headers(),
                timeout=_TIMEOUT,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Failed to fetch analytics.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Connection timeout loading analytics."}

    # ─── GitHub ────────────────────────────────────────────────────────

    def analyze_github(self, github_url) -> dict:
        """Analyze public GitHub profile repository list."""
        try:
            response = requests.post(
                f"{self.base_url}/github/analyze-github",
                json={"github_url": github_url},
                headers=self._get_headers(),
                timeout=30,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "GitHub analysis failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "GitHub analysis timed out."}

    # ─── Career ────────────────────────────────────────────────────────

    def generate_roadmap(self, target_role=None) -> dict:
        """Generate AI-powered career roadmap recommendation paths."""
        try:
            response = requests.post(
                f"{self.base_url}/career/generate-roadmap",
                json={"target_role": target_role},
                headers=self._get_headers(),
                timeout=45,
            )
            if response.status_code == 200:
                return {"success": True, "data": self._safe_json(response)}
            return self._handle_error(response, "Roadmap generation failed.")
        except (Timeout, ConnectionError):
            return {"success": False, "error": "Roadmap generation timed out."}


# Singleton instance used throughout the frontend
api_client = APIClient()
