"""Settings page — app preferences, cache management, and session info with theme switching."""
import streamlit as st
from utils.session import clear_auth
from components.ui import page_header, safe_text


def render_settings_page():
    """Render the application settings page."""

    page_header("Settings", "Manage interview defaults, theme, notifications, and local cache state.", "Workspace")

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        # ── App preferences ───────────────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Interview Preferences</div>
        """, unsafe_allow_html=True)

        # Read or set defaults
        if "pref_difficulty" not in st.session_state:
            st.session_state.pref_difficulty = "Medium"
        if "pref_question_count" not in st.session_state:
            st.session_state.pref_question_count = 10
        if "pref_interview_type" not in st.session_state:
            st.session_state.pref_interview_type = "Technical"

        difficulties = ["Easy", "Medium", "Hard"]
        diff_idx = difficulties.index(st.session_state.pref_difficulty)
        new_diff = st.selectbox("Default Difficulty", difficulties, index=diff_idx, key="settings_diff")

        count_opts = [5, 10, 20]
        count_idx = count_opts.index(st.session_state.pref_question_count) \
            if st.session_state.pref_question_count in count_opts else 1
        new_count = st.selectbox("Default Question Count", count_opts, index=count_idx, key="settings_count")

        interview_types = ["Technical", "Behavioral", "System Design", "Mixed"]
        type_idx = interview_types.index(st.session_state.pref_interview_type) \
            if st.session_state.pref_interview_type in interview_types else 0
        new_type = st.selectbox("Default Interview Type", interview_types, index=type_idx, key="settings_type")

        if st.button("Save Preferences", key="save_prefs", use_container_width=True):
            st.session_state.pref_difficulty = new_diff
            st.session_state.pref_question_count = new_count
            st.session_state.pref_interview_type = new_type
            st.toast("Preferences saved.")

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Theme Preference Switcher ─────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Appearance Theme</div>
        """, unsafe_allow_html=True)

        if "theme_preference" not in st.session_state:
            st.session_state.theme_preference = "Light"

        themes = ["Light", "Dark"]
        theme_idx = themes.index(st.session_state.theme_preference)
        new_theme = st.selectbox("Application Theme", themes, index=theme_idx, key="theme_sel")

        if st.button("Apply Theme Settings", key="save_theme", use_container_width=True):
            st.session_state.theme_preference = new_theme
            st.toast(f"Theme switched to {new_theme} mode.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Notification preferences ──────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Notifications</div>
        """, unsafe_allow_html=True)

        if "notif_tips" not in st.session_state:
            st.session_state.notif_tips = True
        if "notif_progress" not in st.session_state:
            st.session_state.notif_progress = True

        n1 = st.toggle("Show AI Tips & Suggestions", value=st.session_state.notif_tips, key="tog_tips")
        n2 = st.toggle("Show Progress Notifications", value=st.session_state.notif_progress, key="tog_progress")

        if st.button("Save Notification Settings", key="save_notif", use_container_width=True):
            st.session_state.notif_tips = n1
            st.session_state.notif_progress = n2
            st.toast("Notification settings saved.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # ── Cache management ──────────────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Cache & Data</div>
                <p style="font-size:0.825rem;color:var(--text-muted);margin-bottom:16px;">Clear locally cached data to force fresh loads from the server.</p>
        """, unsafe_allow_html=True)

        cache_keys = {
            "cached_career_roadmap": "Career Roadmap",
            "cached_github_analysis": "GitHub Analysis",
            "cached_resume": "Resume Cache",
            "cached_dashboard": "Dashboard Cache",
            "cached_analytics": "Analytics Cache",
        }

        # Show cache status
        for key, label in cache_keys.items():
            val = st.session_state.get(key)
            status = "Cached" if val else "Empty"
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"padding:8px 0;border-bottom:1px solid var(--border);'>"
                f"<span style='font-size:0.825rem;color:var(--text-muted);'>{label}</span>"
                f"<span style='font-size:0.75rem;color:var(--text-faint);'>{status}</span></div>",
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        if st.button("Clear All Caches", key="clear_caches", use_container_width=True):
            for key in cache_keys:
                st.session_state[key] = None
            st.toast("All caches cleared. Next page load will fetch fresh data.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Session info ──────────────────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Session Information</div>
        """, unsafe_allow_html=True)

        user = st.session_state.get("user") or {}
        st.markdown(f"""
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border);">
                    <span style="font-size:0.8rem;color:var(--text-faint);">Logged in as</span>
                    <span style="font-size:0.8rem;color:var(--text-muted);">{safe_text(user.get("name","—"))}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border);">
                    <span style="font-size:0.8rem;color:var(--text-faint);">Email</span>
                    <span style="font-size:0.8rem;color:var(--text-muted);">{safe_text(user.get("email","—"))}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:6px 0;">
                    <span style="font-size:0.8rem;color:var(--text-faint);">Session Token</span>
                    <span style="font-size:0.75rem;color:var(--text-faint);">Stored securely in this Streamlit session</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── About ─────────────────────────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:12px;">About PREPAI</div>
                <div style="font-size:0.825rem;color:var(--text-muted);line-height:1.6;">
                    <div style="margin-bottom:6px;">Version <span style="color:var(--text);font-weight:600;">1.0.0</span></div>
                    <div style="margin-bottom:6px;">Backend: <span style="color:var(--text);">FastAPI + SQLite</span></div>
                    <div style="margin-bottom:6px;">AI Engine: <span style="color:var(--text);">Google Gemini 2.0 Flash</span></div>
                    <div>Built by <span style="color:var(--primary);font-weight:600;">Harshvardhan Mishra</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ── Navigate back ──────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    if st.button("← Back to Dashboard", key="settings_back"):
        st.session_state.current_page = "dashboard"
        st.rerun()
