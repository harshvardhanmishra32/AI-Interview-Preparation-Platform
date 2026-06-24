"""Unified authentication page with login and registration modes."""
import streamlit as st

from components.forms import display_error, display_success
from components.ui import page_header
from utils.api_client import api_client
from utils.session import set_auth


def _password_score(password: str) -> tuple[int, str]:
    checks = [
        len(password) >= 8,
        any(ch.islower() for ch in password),
        any(ch.isupper() for ch in password),
        any(ch.isdigit() for ch in password),
        any(not ch.isalnum() for ch in password),
    ]
    score = sum(checks)
    label = "Strong" if score >= 4 else ("Medium" if score == 3 else "Weak")
    return score, label


def _set_mode(mode: str) -> None:
    st.session_state.auth_mode = mode
    st.session_state.current_page = "register" if mode == "register" else "login"


def _render_login_form() -> None:
    email = st.text_input("Email Address", placeholder="name@example.com", key="auth_login_email")

    show_password = st.checkbox("Show Password", value=False, key="auth_login_show_pwd")
    password = st.text_input(
        "Password",
        type="password" if not show_password else "default",
        placeholder="Enter your password",
        key="auth_login_password",
    )

    remember_me = st.checkbox("Remember me for 7 days", value=True, key="auth_login_remember")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Access Workspace", key="auth_login_submit", use_container_width=True):
        if not email or not password:
            display_error("Please enter both email and password.")
        else:
            with st.spinner("Authenticating..."):
                res = api_client.login(email, password, remember_me=remember_me)
                if res.get("success"):
                    token = res["data"]["access_token"]
                    refresh_token = res["data"].get("refresh_token")
                    st.session_state.token = token
                    profile_res = api_client.get_profile()

                    if profile_res.get("success"):
                        set_auth(token, profile_res["data"], refresh_token=refresh_token)
                        st.session_state.current_page = "dashboard"
                        st.rerun()
                    else:
                        st.session_state.token = None
                        display_error("Authentication succeeded, but failed to load profile data.")
                else:
                    display_error(res.get("error", "Invalid credentials."))


def _render_register_form() -> None:
    name = st.text_input("Full Name", placeholder="John Doe", key="auth_register_name")
    email = st.text_input("Email Address", placeholder="john@example.com", key="auth_register_email")
    education = st.text_input(
        "Education / University",
        placeholder="B.S. in Computer Science",
        key="auth_register_education",
    )

    target_role = st.selectbox(
        "Target Job Role",
        options=[
            "Software Engineer",
            "Data Scientist",
            "Machine Learning Engineer",
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "DevOps Engineer",
            "Product Manager",
            "Other",
        ],
        key="auth_register_target_role",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="At least 8 characters",
        key="auth_register_password",
    )
    if password:
        score, label = _password_score(password)
        st.progress(min(score, 5) / 5)
        st.caption(f"Password strength: {label}")

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Repeat password",
        key="auth_register_confirm_password",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create Free Account", key="auth_register_submit", use_container_width=True):
        if not name or not email or not password or not confirm_password:
            display_error("Please fill in all required fields.")
        elif password != confirm_password:
            display_error("Passwords do not match.")
        elif len(password) < 8:
            display_error("Password must be at least 8 characters long.")
        elif _password_score(password)[0] < 3:
            display_error("Use a stronger password with a mix of uppercase, lowercase, numbers, or symbols.")
        else:
            with st.spinner("Creating account..."):
                reg_res = api_client.register(
                    name=name,
                    email=email,
                    password=password,
                    education=education,
                    target_role=target_role,
                )

                if reg_res.get("success"):
                    st.session_state.reg_success_msg = "Account created successfully. Please log in below."
                    _set_mode("login")
                    st.rerun()
                else:
                    display_error(reg_res.get("error", "Registration failed. Email may already be in use."))


def render_auth_page(default_mode: str = "login") -> None:
    """Render login and registration in the same stable page location."""
    if st.session_state.get("auth_mode") not in {"login", "register"}:
        st.session_state.auth_mode = default_mode

    mode = st.session_state.get("auth_mode", default_mode)
    is_register = mode == "register"

    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown(
            "<div class='app-breadcrumb'>Home &nbsp;&gt;&nbsp; <strong>Account Access</strong></div>",
            unsafe_allow_html=True,
        )
    with col_b2:
        if st.button("Back to Home", key="auth_back_home"):
            st.session_state.current_page = "landing"
            st.rerun()

    page_header(
        "Account Access",
        "Log in or create your account from the same secure workspace entry point.",
        "PREPAI",
    )

    if st.session_state.get("reg_success_msg"):
        display_success(st.session_state.reg_success_msg)
        del st.session_state["reg_success_msg"]

    _, auth_col, _ = st.columns([1, 1.15, 1])
    with auth_col:
        selected = st.radio(
            "Account action",
            ["Log In", "Create Account"],
            index=1 if is_register else 0,
            horizontal=True,
            label_visibility="collapsed",
            key=f"auth_mode_selector_{mode}",
        )
        selected_mode = "register" if selected == "Create Account" else "login"
        if selected_mode != mode:
            _set_mode(selected_mode)
            st.rerun()

        with st.container(border=True):
            if st.session_state.auth_mode == "register":
                st.markdown(
                    "<h2 style='margin:0 0 4px 0;'>Create Free Account</h2>"
                    "<p style='margin:0 0 18px 0;color:var(--text-muted);font-size:0.9rem;'>"
                    "Build your candidate profile and start interview preparation.</p>",
                    unsafe_allow_html=True,
                )
                _render_register_form()
            else:
                st.markdown(
                    "<h2 style='margin:0 0 4px 0;'>Welcome Back</h2>"
                    "<p style='margin:0 0 18px 0;color:var(--text-muted);font-size:0.9rem;'>"
                    "Log in to continue your preparation workspace.</p>",
                    unsafe_allow_html=True,
                )
                _render_login_form()
