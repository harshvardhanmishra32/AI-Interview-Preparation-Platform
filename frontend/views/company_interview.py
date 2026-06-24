"""Company Specific Mock Interview selector page."""
import streamlit as st
from utils.api_client import api_client
from components.forms import display_error
from components.ui import page_header

def render_company_interview():
    """Render company card selection and configurations."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Dashboard &nbsp;&gt;&nbsp; <b>Company Interview</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Dashboard", key="back_to_dash_top"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    
    page_header("Company Interview Mode", "Generate company-aware mock interviews aligned with role, difficulty, and hiring style.", "Interview")
    
    with st.container(border=True):
        st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; font-weight:600; color: var(--text);'>1. Choose Target Employer</h3>", unsafe_allow_html=True)
        
        # Grid of companies
        c_list = [
            {"name": "Google", "icon": "", "color": "#4285F4"},
            {"name": "Amazon", "icon": "", "color": "#FF9900"},
            {"name": "Microsoft", "icon": "", "color": "#F25022"},
            {"name": "TCS", "icon": "", "color": "#E51937"},
            {"name": "Infosys", "icon": "", "color": "#007CC3"},
            {"name": "Accenture", "icon": "", "color": "#A12B93"}
        ]
        
        # Render company selection radio/grid
        selected_company = st.selectbox(
            "Target Employer",
            options=[c["name"] for c in c_list]
        )
        
        # Details card matching selected company
        company_details = next(c for c in c_list if c["name"] == selected_company)
        st.markdown(
            f"""
            <div style='background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 12px; margin-top: 8px; color: var(--text-muted);'>
                Selected target: <b style='color:{company_details["color"]};'>{company_details["name"]}</b>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Configure questions
    with st.container(border=True):
        st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; font-weight:600; color: var(--text);'>2. Configure Mock Parameters</h3>", unsafe_allow_html=True)
        
        interview_type = st.selectbox(
            "Interview Category",
            options=["technical", "hr", "behavioral", "project_based"],
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["easy", "medium", "hard"],
            value="medium",
            format_func=lambda x: x.title(),
            key="company_difficulty_slider"
        )
        
        question_count = st.selectbox(
            "Questions Count",
            options=[5, 10, 20],
            key="company_question_count_select"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Generate Company Interview", key="company_mock_submit"):
            with st.spinner(f"Generating questions aligning with {selected_company}'s values..."):
                res = api_client.generate_questions(
                    interview_type=interview_type,
                    difficulty=difficulty,
                    question_count=question_count,
                    company=selected_company
                )
                
                if res.get("success"):
                    session = res["data"]
                    st.session_state.active_session = session
                    st.session_state.interview_questions = session.get("questions", [])
                    st.session_state.current_question_index = 0
                    st.session_state.interview_answers = {}
                    st.session_state.current_page = "interview_session"
                    st.rerun()
                else:
                    display_error(res.get("error", "Failed to generate mock session. Make sure you have uploaded a resume first."))
