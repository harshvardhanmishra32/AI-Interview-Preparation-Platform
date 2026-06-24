"""Streamlit application main entry point routing user navigation and injecting CSS themes."""
import streamlit as st
import os
from utils.session import init_session_state, is_authenticated
from components.sidebar import render_sidebar

# MUST be first Streamlit call
st.set_page_config(
    page_title="PREPAI - AI Interview Prep Assistant",
    page_icon=":material/school:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Initialize state
init_session_state()

# Import page render functions
from views.landing import render_landing_page
from views.login import render_login_page
from views.register import render_register_page
from views.about_me import render_about_me_page
from views.about_project import render_about_project_page
from views.dashboard import render_dashboard
from views.resume_analyzer import render_resume_analyzer
from views.interview_session import render_interview_session
from views.interview_feedback import render_interview_feedback
from views.analytics import render_analytics_page
from views.interview_history import render_interview_history
from views.career_roadmap import render_career_roadmap
from views.github_analyzer import render_github_analyzer
from views.company_interview import render_company_interview
from views.profile import render_profile_page
from views.settings import render_settings_page

# 1. Load Custom CSS
def load_css():
    theme = st.session_state.get("theme_preference", "Light")
    if theme == "Dark":
        variables = """
        :root {
            --bg:           #0F172A;
            --bg-card:      #1E293B;
            --bg-hover:     #263348;
            --border:       rgba(255, 255, 255, 0.07);
            --border-solid: #2D3748;
            --primary:      #3B82F6;
            --primary-dark: #2563EB;
            --primary-muted:rgba(59, 130, 246, 0.12);
            --text:         #F1F5F9;
            --text-muted:   #94A3B8;
            --text-faint:   #64748B;
            --success:      #22C55E;
            --warning:      #F59E0B;
            --error:        #EF4444;
            --sidebar-bg:   #0B1120;
            --sidebar-text: #F1F5F9;
            --sidebar-text-muted: #94A3B8;
            --radius:       8px;
            --radius-sm:    6px;
            --shadow:       0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
            --shadow-md:    0 4px 16px rgba(0,0,0,0.35);
        }
        """
    else:  # Light Mode (Default SaaS Theme)
        variables = """
        :root {
            --bg:           #F8FAFC;
            --bg-card:      #FFFFFF;
            --bg-hover:     #F1F5F9;
            --border:       #E2E8F0;
            --border-solid: #CBD5E1;
            --primary:      #2563EB;
            --primary-dark: #1D4ED8;
            --primary-muted:rgba(37, 99, 235, 0.08);
            --text:         #0F172A;
            --text-muted:   #64748B;
            --text-faint:   #94A3B8;
            --success:      #22C55E;
            --warning:      #F59E0B;
            --error:        #EF4444;
            --sidebar-bg:   #1E293B;
            --sidebar-text: #F1F5F9;
            --sidebar-text-muted: #94A3B8;
            --radius:       8px;
            --radius-sm:    6px;
            --shadow:       0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
            --shadow-md:    0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        }
        """
    st.markdown(f"<style>{variables}</style>", unsafe_allow_html=True)

    css_path = os.path.join(os.path.dirname(__file__), "styles", "theme.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

load_css()

# 3. Render Sidebar and capture selected navigation
selected_page = render_sidebar()

# 4. Auth Guard redirect rules
protected_pages = [
    "dashboard",
    "resume_analyzer",
    "interview_session",
    "interview_feedback",
    "analytics",
    "interview_history",
    "career_roadmap",
    "github_analyzer",
    "company_interview",
    "profile",
    "settings"
]

if not is_authenticated() and st.session_state.current_page in protected_pages:
    st.session_state.current_page = "landing"
    st.rerun()

# 5. Route views with a controlled app-level fallback
routes = {
    "landing": render_landing_page,
    "login": render_login_page,
    "register": render_register_page,
    "about_me": render_about_me_page,
    "about_project": render_about_project_page,
    "dashboard": render_dashboard,
    "resume_analyzer": render_resume_analyzer,
    "interview_session": render_interview_session,
    "interview_feedback": render_interview_feedback,
    "analytics": render_analytics_page,
    "interview_history": render_interview_history,
    "career_roadmap": render_career_roadmap,
    "github_analyzer": render_github_analyzer,
    "company_interview": render_company_interview,
    "profile": render_profile_page,
    "settings": render_settings_page,
}

try:
    routes.get(st.session_state.current_page, render_landing_page)()
except Exception:
    st.error("Something went wrong while loading this page. Please retry or return to the dashboard.")
    if st.button("Return to Dashboard", key="global_error_dashboard"):
        st.session_state.current_page = "dashboard" if is_authenticated() else "landing"
        st.rerun()
