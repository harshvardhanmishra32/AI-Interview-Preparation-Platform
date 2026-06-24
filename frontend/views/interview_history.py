"""History page for reviewing candidate's past mock interview sessions and grading sheets."""
import streamlit as st
import json
from utils.api_client import api_client
from components.forms import display_error, display_info
from components.ui import page_header, safe_text

def render_interview_history():
    """Render the mock history panel."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Dashboard &nbsp;&gt;&nbsp; <b>Interview History</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Dashboard", key="back_to_dash_top"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    
    page_header("Mock Interview History", "Browse past sessions, answers, scoring, and model feedback.", "History")
    
    # 1. Fetch sessions
    with st.spinner("Fetching interview history..."):
        res = api_client.get_history()
        
    if not res.get("success"):
        display_error("Failed to load interview history.")
        return
        
    sessions = res["data"]
    
    if not sessions:
        display_info("No past interview sessions found. Start a mock interview to populate history details.")
        return
        
    # Check if a specific session detail is selected
    selected_sess_id = st.session_state.get("selected_history_session_id")
    
    if selected_sess_id is not None:
        # DETAIL VIEW FOR SELECTED SESSION
        if st.button("Back to History List", key="history_back_to_list"):
            st.session_state.selected_history_session_id = None
            st.rerun()
            
        with st.spinner("Loading session detailed report..."):
            detail_res = api_client.get_interview(selected_sess_id)
            
        if not detail_res.get("success"):
            display_error("Could not load session details.")
            return
            
        session = detail_res["data"]
        company_str = f" @ {session.get('company')}" if session.get("company") else ""
        
        st.markdown(
            f"""
            <div style='background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: var(--shadow);'>
                <h3 style='margin:0 0 8px 0; font-size:1.25rem; color: var(--text);'>{safe_text(session.get('interview_type','').replace('_',' ').title())} Interview Session{safe_text(company_str)}</h3>
                <div style='font-size:0.85rem; color: var(--text-muted);'>Role: {safe_text(session.get('role'))} | Difficulty: {safe_text(session.get('difficulty','').title())} | Status: {safe_text(session.get('status','').title())}</div>
                <div style='font-size:0.85rem; color: var(--text-faint); margin-top:4px;'>Conducted on {safe_text(session.get('created_at'))}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        questions = session.get("questions", [])
        for idx, q in enumerate(questions):
            ans = q.get("answer")
            
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                        <span style='font-size:0.8rem; color: var(--primary); font-weight:600; text-transform:uppercase;'>Question {idx + 1} - {safe_text(q.get('topic'))}</span>
                    </div>
                    <h4 style='margin:0 0 12px 0; font-size:1.05rem; color: var(--text);'>{safe_text(q.get('question_text'))}</h4>
                    """,
                    unsafe_allow_html=True
                )
                
                if ans:
                    score = ans.get("score")
                    score_color = "var(--success)" if (score and score >= 7) else ("var(--warning)" if (score and score >= 4) else "var(--error)")
                    score_val = f"{score}/10" if score is not None else "Pending"
                    
                    # Check if feedback payload is json string
                    eval_payload = {}
                    if ans.get("feedback"):
                        try:
                            # feedback is stringified JSON response or text
                            if ans["feedback"].startswith("{"):
                                eval_payload = json.loads(ans["feedback"])
                            else:
                                eval_payload = {"feedback": ans["feedback"]}
                        except Exception:
                            eval_payload = {"feedback": ans["feedback"]}
                            
                    st.markdown(
                        f"""
                        <div style='background: var(--bg); border: 1px solid var(--border); border-radius:6px; padding:12px; margin-bottom:12px;'>
                            <div style='font-size:0.75rem; color: var(--text-muted); font-weight:500; margin-bottom:4px;'>YOUR RESPONSE:</div>
                            <div style='font-size:0.85rem; color: var(--text); font-style:italic;'>{safe_text(ans.get('answer_text'))}</div>
                        </div>
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; color: var(--text);'>
                            <span style='font-weight:600; font-size:0.9rem;'>AI Score: <span style='color:{score_color}; font-weight:700;'>{score_val}</span></span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Expandable details
                    st.markdown(f"**Technical Accuracy:** {eval_payload.get('technical_accuracy', 'N/A')}")
                    st.markdown(f"**Suggestions:** {', '.join(ans.get('suggestions', [])) or 'None'}")
                    st.markdown(f"**Missing Concepts:** {', '.join(ans.get('missing_concepts', [])) or 'None'}")
                    with st.expander("Ideal Answer"):
                        st.write(ans.get("ideal_answer", "Not provided."))
                else:
                    st.write("Candidate did not answer this question.")
            
    else:
        # LIST VIEW OF SESSIONS
        for s in sessions:
            q_list = s.get("questions", [])
            completed_count = sum([1 for q in q_list if q.get("answer") is not None])
            
            # Find average score
            valid_scores = [q["answer"]["score"] for q in q_list if (q.get("answer") and q["answer"].get("score") is not None)]
            avg_score = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else None
            
            avg_score_lbl = f"Grade: {avg_score}/10" if avg_score is not None else ("In Progress" if s.get("status") == "in_progress" else "N/A")
            score_color = "var(--success)" if (avg_score and avg_score >= 7) else ("var(--warning)" if (avg_score and avg_score >= 4) else "var(--error)")
            
            with st.container(border=True):
                col_info, col_action = st.columns([4, 1])
                
                with col_info:
                    company_lbl = f" @ {s['company']}" if s.get("company") else ""
                    st.markdown(
                        f"""
                        <h3 style='margin:0 0 6px 0; font-size:1.15rem; color: var(--text);'>{s['interview_type'].title()} Interview{company_lbl}</h3>
                        <div style='font-size:0.85rem; color: var(--text-muted);'>Role: {s['role']} | Difficulty: {s['difficulty'].title()} | Status: {s['status'].title()}</div>
                        <div style='font-size:0.8rem; color: var(--primary); font-weight:600; margin-top:4px;'>{completed_count} of {len(q_list)} Questions Answered | <span style='color:{score_color if avg_score else "var(--warning)"};'>{avg_score_lbl}</span></div>
                        <div style='font-size:0.75rem; color: var(--text-faint); margin-top:2px;'>Conducted on {s['created_at'].replace('T',' ').split('.')[0]}</div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                with col_action:
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    if st.button("Review", key=f"history_review_btn_{s['id']}", use_container_width=True):
                        st.session_state.selected_history_session_id = s["id"]
                        st.rerun()
