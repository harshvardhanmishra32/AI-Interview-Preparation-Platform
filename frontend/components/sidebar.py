"""Sidebar component — professional dark nav with active state highlighting."""
import streamlit as st
from utils.session import is_authenticated, clear_auth


# Navigation items: (label, page_key, icon)
_NAV_MAIN = [
    ("Dashboard", "dashboard", "Overview"),
    ("Resume Analyzer", "resume_analyzer", "Resume"),
    ("Mock Interview", "interview_session", "Mock"),
    ("Interview Feedback", "interview_feedback", "Review"),
    ("Company Interview", "company_interview", "Company"),
    ("Interview History", "interview_history", "History"),
]

_NAV_TOOLS = [
    ("Analytics", "analytics", "Data"),
    ("Career Roadmap", "career_roadmap", "Plan"),
    ("GitHub Analyzer", "github_analyzer", "Code"),
]

_NAV_ACCOUNT = [
    ("Profile", "profile", "User"),
    ("Settings", "settings", "Prefs"),
    ("About Me", "about_me", "Bio"),
    ("About Project", "about_project", "Case"),
]

_NAV_GUEST = [
    ("Home", "landing", "▪"),
    ("About Me", "about_me", "▪"),
    ("About Project", "about_project", "▪"),
]


def _nav_button(label: str, page: str, current: str, key_suffix: str = ""):
    """Render a sidebar nav button with active state highlighting."""
    is_active = current == page
    btn_key = f"nav_{page}_{key_suffix}" if key_suffix else f"nav_{page}"

    if is_active:
        st.markdown(
            f"""
            <div style="margin:2px 4px;padding:8px 12px;border-radius:6px;
                background:rgba(59,130,246,0.14);border-left:2px solid #3B82F6;
                color:#BFDBFE;font-size:0.875rem;font-weight:650;">
                {label}
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    clicked = st.button(label, key=btn_key, use_container_width=True)

    if clicked:
        st.session_state.current_page = page
        st.rerun()


def _section_label(text: str):
    st.markdown(
        f"<div style='font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;"
        f"color:#475569;padding:12px 12px 4px 12px;margin-top:4px;'>{text}</div>",
        unsafe_allow_html=True
    )


def render_sidebar():
    """Render the complete sidebar navigation."""
    with st.sidebar:
        # ── Logo ─────────────────────────────────────────────────────────
        st.markdown(
            """<div style='padding:20px 12px 16px 12px;border-bottom:1px solid rgba(255,255,255,0.05);'>
                <div style='display:flex;align-items:center;gap:10px;'>
                    <div style='width:30px;height:30px;border-radius:8px;background:#2563EB;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:0.8rem;'>AI</div>
                    <div>
                        <div style='font-size:0.95rem;font-weight:800;color:#F8FAFC;line-height:1;'>PREPAI</div>
                        <div style='font-size:0.68rem;color:#94A3B8;margin-top:4px;'>Interview readiness OS</div>
                    </div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

        current = st.session_state.get("current_page", "landing")

        if is_authenticated():
            user = st.session_state.user or {}
            name = user.get("name", "User")
            role = user.get("target_role") or "Candidate"
            email = user.get("email", "")
            initials = "".join([w[0].upper() for w in name.split()[:2]])

            # ── User card ─────────────────────────────────────────────────
            st.markdown(f"""
                <div style='margin:12px 8px 8px 8px;padding:12px;background:rgba(255,255,255,0.03);
                    border:1px solid rgba(255,255,255,0.06);border-radius:8px;'>
                    <div style='display:flex;align-items:center;gap:10px;'>
                        <div style='width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#3B82F6,#6366F1);
                            display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;
                            color:#fff;flex-shrink:0;'>{initials}</div>
                        <div style='min-width:0;'>
                            <div style='font-size:0.825rem;font-weight:600;color:#E2E8F0;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{name}</div>
                            <div style='font-size:0.7rem;color:#3B82F6;font-weight:500;'>{role}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # ── Main nav ──────────────────────────────────────────────────
            _section_label("Main")
            for label, page, _ in _NAV_MAIN:
                _nav_button(label, page, current)

            # ── Tools nav ─────────────────────────────────────────────────
            _section_label("Tools")
            for label, page, _ in _NAV_TOOLS:
                _nav_button(label, page, current)

            # ── Account nav ───────────────────────────────────────────────
            _section_label("Account")
            for label, page, _ in _NAV_ACCOUNT:
                _nav_button(label, page, current)

            # ── Sign Out ──────────────────────────────────────────────────
            st.markdown(
                "<hr style='border:none;border-top:1px solid rgba(255,255,255,0.05);margin:12px 0 8px 0;'>",
                unsafe_allow_html=True,
            )
            st.markdown("""
                <style>
                div[data-testid="stSidebar"] div[data-testid="stButton"]:last-child button {
                    background: rgba(239, 68, 68, 0.08) !important;
                    color: #FCA5A5 !important;
                    border: 1px solid rgba(239, 68, 68, 0.2) !important;
                    border-radius: 6px !important;
                }
                div[data-testid="stSidebar"] div[data-testid="stButton"]:last-child button:hover {
                    background: rgba(239, 68, 68, 0.15) !important;
                    color: #FEE2E2 !important;
                }
                </style>
            """, unsafe_allow_html=True)
            if st.button("Logout", key="nav_signout", use_container_width=True):
                clear_auth()
                st.rerun()

        else:
            # ── Guest nav ─────────────────────────────────────────────────
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            for label, page, _ in _NAV_GUEST:
                _nav_button(label, page, current, key_suffix="guest")

            st.markdown(
                "<hr style='border:none;border-top:1px solid rgba(255,255,255,0.05);margin:12px 0 8px 0;'>",
                unsafe_allow_html=True,
            )
            if st.button("Log In", key="nav_login_guest", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.session_state.current_page = "login"
                st.rerun()
            if st.button("Sign Up", key="nav_register_guest", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.session_state.current_page = "register"
                st.rerun()

    return st.session_state.get("current_page", "landing")
