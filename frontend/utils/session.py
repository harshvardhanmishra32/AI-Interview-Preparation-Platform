"""Session state utilities for managing user authentication and active mock interviews."""
import streamlit as st


def init_session_state():
    """Ensure all required session state variables exist on application reload."""
    defaults = {
        "token": None,
        "refresh_token": None,
        "user": None,
        "current_page": "landing",
        # Interview session data
        "active_session": None,
        "interview_questions": [],
        "current_question_index": 0,
        "interview_answers": {},
        "interview_start_time": None,
        # Page-level caches (must be cleared on logout)
        "cached_career_roadmap": None,
        "cached_github_analysis": None,
        "cached_resume": None,
        "cached_dashboard": None,
        "cached_analytics": None,
        # UI state
        "selected_history_session_id": None,
        "reg_success_msg": None,
        "theme_preference": "Light",
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def is_authenticated() -> bool:
    """Return whether the current session is logged in (token present)."""
    return st.session_state.get("token") is not None


def set_auth(token: str, user_profile: dict, refresh_token: str | None = None):
    """Save authorization token and profile data in the session state."""
    st.session_state.token = token
    st.session_state.refresh_token = refresh_token
    st.session_state.user = user_profile
    st.session_state.current_page = "dashboard"


def clear_auth():
    """Clear all credentials, caches, and return to landing page."""
    # Auth state
    st.session_state.token = None
    st.session_state.refresh_token = None
    st.session_state.user = None
    st.session_state.current_page = "landing"
    # Interview session state
    st.session_state.active_session = None
    st.session_state.interview_questions = []
    st.session_state.current_question_index = 0
    st.session_state.interview_answers = {}
    st.session_state.interview_start_time = None
    # Page caches — CRITICAL: prevents cross-user data leakage
    st.session_state.cached_career_roadmap = None
    st.session_state.cached_github_analysis = None
    st.session_state.cached_resume = None
    st.session_state.cached_dashboard = None
    st.session_state.cached_analytics = None
    # UI state
    st.session_state.selected_history_session_id = None
    st.session_state.reg_success_msg = None


def get_token() -> str | None:
    """Retrieve auth bearer token."""
    return st.session_state.get("token")
