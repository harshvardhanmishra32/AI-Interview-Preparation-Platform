"""Public landing page for PREPAI."""
import streamlit as st
from components.logo import get_logo_svg
from components.ui import safe_text


def _section_heading(label: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div style="margin:56px 0 22px 0;text-align:center;">
            <div class="page-eyebrow">{safe_text(label)}</div>
            <h2 style="font-size:1.65rem;font-weight:750;color:var(--text);margin:0;">{safe_text(title)}</h2>
            <p style="max-width:680px;margin:10px auto 0 auto;color:var(--text-muted);font-size:0.94rem;">{safe_text(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _feature(title: str, body: str, accent: str = "#2563EB") -> None:
    st.markdown(
        f"""
        <div class="surface-card" style="height:100%;border-top:2px solid {accent};">
            <div style="font-weight:650;color:var(--text);font-size:0.98rem;margin-bottom:8px;">{safe_text(title)}</div>
            <div style="font-size:0.84rem;color:var(--text-muted);line-height:1.65;">{safe_text(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing_page():
    """Render a polished SaaS landing page."""
    nav_col, _, cta_col = st.columns([1.6, 1.4, 5])
    with nav_col:
        st.markdown(get_logo_svg(height=32, show_text=True), unsafe_allow_html=True)
    with cta_col:
        c1, c2, c3 = st.columns([0.8, 0.8, 1.7])
        with c1:
            if st.button("Log In", key="landing_login_nav", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.session_state.current_page = "login"
                st.rerun()
        with c2:
            if st.button("Sign Up", key="landing_register_nav", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.session_state.current_page = "register"
                st.rerun()
        with c3:
            if st.button("Create Free Account", key="landing_create_account_nav", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.session_state.current_page = "register"
                st.rerun()

    st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <section class="landing-hero">
            <div style="display:grid;grid-template-columns:minmax(0,0.92fr) minmax(440px,1.08fr);gap:34px;align-items:center;">
                <div>
                    <div class="page-eyebrow">AI Interview Readiness OS</div>
                    <h1 style="font-size:3.25rem;line-height:1.05;font-weight:850;margin:0 0 18px 0;letter-spacing:0;">
                        Turn interview prep into measurable hiring readiness.
                    </h1>
                    <p class="hero-muted" style="font-size:1rem;line-height:1.72;margin:0 0 24px 0;max-width:560px;">
                        A focused workspace for resume signal, mock interview scoring, portfolio review, career planning, and analytics. Built to show product thinking, engineering depth, and recruiter-ready execution.
                    </p>
                </div>
                <div class="product-preview">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
                        <div class="preview-topbar" style="width:58px;"></div>
                        <div class="preview-topbar" style="width:38px;"></div>
                        <div class="preview-topbar" style="width:46px;"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">
                        <div>
                            <div style="font-weight:800;font-size:1rem;">Dashboard</div>
                            <div style="font-size:0.76rem;color:#64748B !important;">Candidate readiness report</div>
                        </div>
                        <span class="badge badge-green">Production demo</span>
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px;">
                        <div style="border:1px solid #E2E8F0;border-radius:8px;padding:12px;background:#FFFFFF;"><div style="font-size:0.68rem;color:#64748B !important;font-weight:700;">SESSIONS</div><div style="font-size:1.55rem;font-weight:850;">24</div></div>
                        <div style="border:1px solid #E2E8F0;border-radius:8px;padding:12px;background:#FFFFFF;"><div style="font-size:0.68rem;color:#64748B !important;font-weight:700;">GROWTH</div><div style="font-size:1.55rem;font-weight:850;color:#16A34A !important;">+18%</div></div>
                        <div style="border:1px solid #E2E8F0;border-radius:8px;padding:12px;background:#FFFFFF;"><div style="font-size:0.68rem;color:#64748B !important;font-weight:700;">FOCUS</div><div style="font-size:1.05rem;font-weight:800;">System Design</div></div>
                    </div>
                    <div style="display:grid;grid-template-columns:1.1fr 0.9fr;gap:12px;">
                        <div>
                            <div class="mini-chart">
                                <span style="height:42%;"></span><span style="height:48%;"></span><span style="height:54%;"></span><span style="height:62%;"></span><span style="height:68%;"></span><span style="height:78%;"></span><span style="height:84%;"></span>
                            </div>
                        </div>
                        <div style="border:1px solid #E2E8F0;border-radius:8px;padding:12px;background:#F8FAFC;">
                            <div style="font-size:0.74rem;color:#64748B !important;font-weight:700;margin-bottom:8px;">AI RECOMMENDATIONS</div>
                            <div class="preview-row primary" style="width:94%;height:8px;"></div>
                            <div class="preview-row success" style="width:78%;height:8px;"></div>
                            <div class="preview-row warn" style="width:88%;height:8px;"></div>
                            <div class="preview-row" style="width:65%;height:8px;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    _section_heading("Features", "Everything serious candidates need", "A complete preparation loop from raw profile to measurable interview improvement.")
    features = [
        ("AI Mock Interview Demo", "Generate role, difficulty, and company-aware questions with answer scoring and model feedback.", "#2563EB"),
        ("Resume Analyzer Demo", "Parse PDF resumes, identify skills, detect gaps, and receive recruiter-grade improvement suggestions.", "#22C55E"),
        ("GitHub Analyzer Demo", "Review repositories, language distribution, contribution signals, and project-specific questions.", "#6366F1"),
        ("Career Roadmap Preview", "Turn resume gaps and interview analytics into learning milestones, certifications, and project plans.", "#F59E0B"),
        ("Analytics Workspace", "Track topic performance, weekly growth, interview history, and skill momentum with clean charts.", "#2563EB"),
        ("Company Interview Mode", "Focus preparation for Google, Amazon, Microsoft, TCS, Infosys, Accenture, and more.", "#EF4444"),
    ]
    cols = st.columns(3)
    for idx, item in enumerate(features):
        with cols[idx % 3]:
            _feature(*item)

    _section_heading("Product Demo", "A preparation workflow that feels connected", "Each tool produces data that improves the next tool, so the platform behaves like one product.")
    demo_cols = st.columns(4)
    demo_steps = [
        ("1. Upload", "Resume profile and skill graph are created."),
        ("2. Practice", "Mock sessions adapt to role, company, and background."),
        ("3. Review", "Scores, feedback, and missed concepts are saved."),
        ("4. Improve", "Roadmap and analytics recommend the next move."),
    ]
    for col, (title, body) in zip(demo_cols, demo_steps):
        with col:
            _feature(title, body)

    _section_heading("Success Metrics", "Built for measurable progress", "Recruiters care about proof. PREPAI surfaces preparation outcomes clearly.")
    metric_cols = st.columns(4)
    metrics = [("95+", "Target Lighthouse score"), ("10/10", "Answer scoring scale"), ("5", "Core evaluation criteria"), ("7 days", "Remember-me session option")]
    for col, (value, label) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"<div class='kpi-card'><div class='kpi-value'>{safe_text(value)}</div><div class='kpi-sub'>{safe_text(label)}</div></div>",
                unsafe_allow_html=True,
            )

    _section_heading("Testimonials", "Designed for recruiter confidence", "A professional presentation layer for a practical full-stack AI product.")
    t1, t2, t3 = st.columns(3)
    testimonials = [
        ("The dashboard makes progress obvious without making the product feel busy.", "Frontend Engineer"),
        ("The resume, GitHub, and interview flows connect in a way that tells a candidate story.", "Technical Recruiter"),
        ("The backend fallbacks make it demo-ready even when AI services are unavailable.", "Full Stack Reviewer"),
    ]
    for col, (quote, role) in zip([t1, t2, t3], testimonials):
        with col:
            _feature(f'"{quote}"', role)

    _section_heading("FAQ", "Questions candidates and reviewers ask", "Clear answers for setup, data, and product expectations.")
    faqs = [
        ("Does it require Gemini?", "No. Gemini improves output quality, but local fallbacks keep demos functional without an API key."),
        ("Is authentication protected?", "The app uses bcrypt password hashing, JWT bearer auth, protected API routes, and session cleanup on logout."),
        ("Can it be extended?", "Yes. The API/service/database structure separates concerns cleanly for future React, Postgres, or deployment upgrades."),
    ]
    for question, answer in faqs:
        with st.expander(question):
            st.write(answer)

    st.markdown(
        """
        <footer style="margin-top:56px;padding:24px 0;border-top:1px solid var(--border);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;">
            <span style="font-size:0.82rem;color:var(--text-faint);">PREPAI - AI Interview Preparation Platform</span>
            <span style="font-size:0.82rem;color:var(--text-faint);">Built by Harshvardhan Mishra</span>
        </footer>
        """,
        unsafe_allow_html=True,
    )
