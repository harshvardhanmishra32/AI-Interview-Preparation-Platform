"""Profile page — view and update user details, change password."""
import streamlit as st
from utils.api_client import api_client
from utils.session import clear_auth
from components.ui import page_header, safe_text


def render_profile_page():
    """Render the user profile management page."""
    user = st.session_state.get("user") or {}

    # ── Page header ─────────────────────────────────────────────────────
    page_header("Profile", "Manage your identity, target role, and security settings.", "Account")

    # ── Profile section ──────────────────────────────────────────────────
    col_profile, col_security = st.columns([1, 1], gap="large")

    with col_profile:
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Account Information</div>
        """, unsafe_allow_html=True)

        # Avatar initials
        name = user.get("name", "U")
        initials = "".join([w[0].upper() for w in name.split()[:2]])
        email = user.get("email", "")
        role = user.get("target_role") or "Not set"
        education = user.get("education") or ""
        joined = user.get("created_at", "")[:10] if user.get("created_at") else "—"

        st.markdown(f"""
            <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid var(--border);">
                <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,var(--primary),#6366F1);display:flex;align-items:center;justify-content:center;font-size:1.2rem;font-weight:700;color:#fff;flex-shrink:0;">{initials}</div>
                <div>
                    <div style="font-size:1rem;font-weight:600;color:var(--text);">{safe_text(name)}</div>
                    <div style="font-size:0.825rem;color:var(--text-muted);margin-top:2px;">{safe_text(email)}</div>
                    <div style="font-size:0.75rem;color:var(--text-faint);margin-top:3px;">Member since {joined}</div>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:4px;">
                <div><div style="font-size:0.7rem;color:var(--text-faint);margin-bottom:3px;">TARGET ROLE</div><div style="font-size:0.875rem;color:var(--text-muted);">{safe_text(role)}</div></div>
                <div><div style="font-size:0.7rem;color:var(--text-faint);margin-bottom:3px;">EDUCATION</div><div style="font-size:0.875rem;color:var(--text-muted);">{safe_text(education or "—")}</div></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Edit profile form ─────────────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Edit Profile</div>
        """, unsafe_allow_html=True)

        with st.form("profile_form", clear_on_submit=False):
            new_name = st.text_input("Full Name", value=user.get("name", ""), key="profile_name")
            new_email = st.text_input("Email Address", value=user.get("email", "") or "", key="profile_email")
            role_options = [
                "Software Engineer", "Frontend Engineer", "Backend Engineer",
                "Full Stack Engineer", "Data Scientist", "ML Engineer",
                "DevOps Engineer", "Product Manager", "Other"
            ]
            current_role = user.get("target_role") or "Software Engineer"
            role_idx = role_options.index(current_role) if current_role in role_options else 0
            new_role = st.selectbox("Target Role", role_options, index=role_idx, key="profile_role")
            new_education = st.text_input("Education", value=user.get("education", "") or "", key="profile_edu",
                                          placeholder="e.g. B.Tech Computer Science, MIT")

            submitted = st.form_submit_button("Save Changes", use_container_width=True)
            if submitted:
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    with st.spinner("Saving..."):
                        res = api_client.update_profile(
                            new_name.strip(),
                            new_education.strip() or None,
                            new_role,
                            email=new_email.strip(),
                        )
                    if res.get("success"):
                        # Update session state with new profile
                        st.session_state.user = res["data"]
                        st.toast("Profile updated successfully.")
                        st.rerun()
                    else:
                        st.error(res.get("error", "Update failed."))

        st.markdown("</div>", unsafe_allow_html=True)

    with col_security:
        # ── Change password ───────────────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Change Password</div>
        """, unsafe_allow_html=True)

        with st.form("password_form", clear_on_submit=True):
            current_pw = st.text_input("Current Password", type="password", key="pw_current")
            new_pw = st.text_input("New Password", type="password", key="pw_new",
                                   help="Minimum 8 characters")
            confirm_pw = st.text_input("Confirm New Password", type="password", key="pw_confirm")

            pw_submitted = st.form_submit_button("Update Password", use_container_width=True)
            if pw_submitted:
                if not current_pw:
                    st.error("Please enter your current password.")
                elif len(new_pw) < 8:
                    st.error("New password must be at least 8 characters.")
                elif new_pw != confirm_pw:
                    st.error("New passwords do not match.")
                else:
                    with st.spinner("Updating password..."):
                        res = api_client.change_password(current_pw, new_pw)
                    if res.get("success"):
                        st.toast("Password changed successfully.")
                        st.success("Password updated. You will be logged out for security.")
                        import time; time.sleep(2)
                        clear_auth()
                        st.rerun()
                    else:
                        st.error(res.get("error", "Password change failed."))

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Account stats ─────────────────────────────────────────────────
        st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:24px;box-shadow:var(--shadow);">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Quick Actions</div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("View Analytics", key="profile_to_analytics", use_container_width=True):
                st.session_state.current_page = "analytics"
                st.rerun()
            if st.button("Career Roadmap", key="profile_to_roadmap", use_container_width=True):
                st.session_state.current_page = "career_roadmap"
                st.rerun()
        with col_b:
            if st.button("Interview History", key="profile_to_history", use_container_width=True):
                st.session_state.current_page = "interview_history"
                st.rerun()
            if st.button("Dashboard", key="profile_to_dash", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Danger zone ───────────────────────────────────────────────────
        st.markdown("""
            <div style="background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.15);border-radius:10px;padding:20px;margin-top:4px;">
                <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:#EF4444;margin-bottom:10px;">Danger Zone</div>
                <p style="font-size:0.8rem;color:var(--text-muted);margin-bottom:12px;">Sign out of your account. Your data will remain saved.</p>
        """, unsafe_allow_html=True)

        if st.button("Logout", key="profile_logout", use_container_width=True):
            clear_auth()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
