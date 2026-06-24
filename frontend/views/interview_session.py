"""Mock Interview session execution page simulator."""
from datetime import datetime, timezone
import streamlit as st
from utils.api_client import api_client
from components.forms import display_error, display_success, display_info
from components.ui import page_header, section_title, safe_text

def render_interview_session():
    """Render the mock interview selector interface and simulator flow."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Dashboard &nbsp;&gt;&nbsp; <b>Mock Interview</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Dashboard", key="back_to_dash_top"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    
    page_header("Mock Interview Simulator", "Generate tailored questions, track progress, and receive structured AI evaluation.", "Interview")
    
    # Check if a session is currently active
    if st.session_state.active_session is None:
        st.markdown("<p style='color: var(--text-muted); font-size: 0.95rem; margin-bottom: 24px;'>Start a personalized mock interview. AI will generate questions based on your background.</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            section_title("Configure Mock Session", "Choose the practice format that best matches your next interview.")
            
            interview_type = st.selectbox(
                "Interview Type",
                options=["technical", "hr", "behavioral", "project_based"],
                format_func=lambda x: x.replace("_", " ").title()
            )
            
            difficulty = st.select_slider(
                "Difficulty Level",
                options=["easy", "medium", "hard"],
                value="medium",
                format_func=lambda x: x.title()
            )
            
            question_count = st.selectbox(
                "Number of Questions",
                options=[5, 10, 20]
            )
            
            company = st.text_input("Target Company (Optional)", placeholder="e.g. Google, Amazon, Microsoft")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Start Mock Interview", key="mock_setup_submit", use_container_width=True):
                with st.spinner("Generating interview questions tailored to your profile..."):
                    res = api_client.generate_questions(
                        interview_type=interview_type,
                        difficulty=difficulty,
                        question_count=question_count,
                        company=company if company.strip() else None
                    )
                    
                    if res.get("success"):
                        session = res["data"]
                        st.session_state.active_session = session
                        st.session_state.interview_questions = session.get("questions", [])
                        st.session_state.current_question_index = 0
                        st.session_state.interview_answers = {}
                        st.session_state.interview_start_time = datetime.now(timezone.utc)
                        st.rerun()
                    else:
                        display_error(res.get("error", "Failed to generate mock session. Make sure you have uploaded a resume first."))
        
    else:
        # ACTIVE INTERVIEW SIMULATOR FLOW
        session = st.session_state.active_session
        questions = st.session_state.interview_questions
        idx = st.session_state.current_question_index
        
        if idx >= len(questions):
            # Interview ended
            # Reset active session
            st.session_state.active_session = None
            st.session_state.current_page = "interview_feedback"
            # Keep index/answers for feedback view
            st.rerun()
            
        # UI Header details
        q_count = len(questions)
        company_str = f" @ {session.get('company')}" if session.get("company") else ""
        start_time = st.session_state.get("interview_start_time")
        elapsed = ""
        if start_time:
            seconds = int((datetime.now(timezone.utc) - start_time).total_seconds())
            elapsed = f" | Time: {seconds // 60:02d}:{seconds % 60:02d}"
        st.markdown(
            f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;'>
                <div style='font-size:0.95rem; color: var(--text-muted);'>
                    Role: <span style='color: var(--primary); font-weight:600;'>{safe_text(session.get('role', 'Candidate'))}</span> {safe_text(company_str)} | Type: <span style='color: var(--primary);'>{safe_text(session.get('interview_type','').replace('_',' ').title())}</span>{safe_text(elapsed)}
                </div>
                <div style='font-weight: 700; color: var(--warning);'>Question {idx + 1} of {q_count}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Progress Bar
        st.progress((idx) / q_count)
        
        current_q = questions[idx]
        
        # Display Question Card
        with st.container(border=True):
            st.markdown(
                f"""
                <div style='display:flex; gap:10px; margin-bottom: 12px;'>
                    <span class='badge badge-primary'>{safe_text(current_q.get('topic', 'General'))}</span>
                    <span class='badge badge-warning'>{safe_text(current_q.get('difficulty', '').title())}</span>
                </div>
                <h3 style='margin:0 0 16px 0; font-size:1.3rem; font-weight:600; line-height: 1.5; color: var(--text);'>{safe_text(current_q.get('question_text'))}</h3>
                """,
                unsafe_allow_html=True
            )
            
            # Input Text Area
            answer_text = st.text_area("Your Response", placeholder="Type your answer here. Provide a detailed explanation...", height=180, key=f"q_ans_input_{current_q.get('id')}")
        
        # Row of Buttons
        b_col1, b_col2, b_col3, b_col4 = st.columns([2, 1, 1, 2])
        
        with b_col1:
            if st.button("Submit & Evaluate Answer", key="simulator_btn_submit", use_container_width=True):
                if not answer_text.strip():
                    st.warning("Please type an answer before submitting.")
                else:
                    with st.spinner("Submitting answer and preparing evaluation..."):
                        sub_res = api_client.submit_answer(
                            question_id=current_q.get("id"),
                            answer_text=answer_text
                        )
                        
                        if sub_res.get("success"):
                            # Cache evaluation
                            st.session_state.interview_answers[idx] = {
                                "question": current_q,
                                "user_answer": answer_text,
                                "evaluation": sub_res["data"]
                            }
                            # Move to next
                            st.session_state.current_question_index += 1
                            st.rerun()
                        else:
                            display_error(sub_res.get("error", "Evaluation failed."))
                            
        with b_col2:
            if st.button("Skip Question", key="simulator_btn_skip", use_container_width=True):
                with st.spinner("Skipping question..."):
                    sub_res = api_client.submit_answer(
                        question_id=current_q.get("id"),
                        answer_text="[Skipped]"
                    )
                    
                    if sub_res.get("success"):
                        st.session_state.interview_answers[idx] = {
                            "question": current_q,
                            "user_answer": "[Skipped]",
                            "evaluation": sub_res["data"]
                        }
                        st.session_state.current_question_index += 1
                        st.rerun()
                    else:
                        display_error(sub_res.get("error", "Failed to skip question on backend."))
                
        with b_col3:
            # End early
            if st.button("End Session", key="simulator_btn_end", use_container_width=True):
                st.session_state.active_session = None
                st.session_state.current_page = "interview_feedback"
                st.rerun()
                
        # Display guidelines
        st.markdown("<br>", unsafe_allow_html=True)
        display_info("Use a structured answer: context, approach, trade-offs, and verification.")
