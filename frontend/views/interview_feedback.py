"""Post interview mock evaluation review feedback page."""
import streamlit as st
import json
from components.cards import score_card
from components.forms import display_info
from components.ui import page_header, safe_text

def render_interview_feedback():
    """Render the candidate's post session mock grading sheet."""
    page_header("Mock Evaluation Summary", "Review scoring, missed concepts, suggestions, and model answer references.", "Feedback")
    
    answers = st.session_state.interview_answers
    
    if not answers:
        st.warning("No feedback data available. Take a mock interview first.")
        if st.button("Start Interview Session", key="feedback_go_mock"):
            st.session_state.current_page = "interview_session"
            st.rerun()
        return
        
    # Calculate average score of answers
    valid_scores = [val["evaluation"].get("score", 0.0) for val in answers.values() if val.get("evaluation")]
    avg_score = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else 0.0
    
    # Large score visualization
    score_card(avg_score, "Mock Grade")
    
    st.markdown("<br><hr style='border-color: var(--border);'><br>", unsafe_allow_html=True)
    
    # Display each question's evaluation details
    for idx, item in answers.items():
        q = item["question"]
        ans_text = item["user_answer"]
        eval_data = item["evaluation"]
        
        # In case the feedback string was returned as a json string
        if isinstance(eval_data.get("feedback"), str) and eval_data["feedback"].startswith("{"):
            try:
                eval_data = json.loads(eval_data["feedback"])
            except Exception:
                pass
                
        score = eval_data.get("score", 5.0)
        score_color = "var(--success)" if score >= 7 else ("var(--warning)" if score >= 4 else "var(--error)")
        
        with st.container(border=True):
            st.markdown(
                f"""
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                    <span style='font-size:0.8rem; color: var(--primary); font-weight:600; text-transform:uppercase;'>Question {idx + 1} - {safe_text(q.get('topic'))}</span>
                    <span style='font-weight:700; color:{score_color}; font-size: 1.1rem;'>Score: {score}/10</span>
                </div>
                <h4 style='margin:0 0 12px 0; font-size:1.1rem; line-height: 1.4; color: var(--text);'>{safe_text(q.get('question_text'))}</h4>
                
                <div style='background: var(--bg); border: 1px solid var(--border); border-radius:6px; padding:12px; margin-bottom:16px;'>
                    <div style='font-size:0.75rem; color: var(--text-muted); font-weight:500; margin-bottom:4px; text-transform:uppercase;'>Your Response:</div>
                    <div style='font-size:0.85rem; color: var(--text); font-style:italic;'>{safe_text(ans_text)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Detailed feedback criteria
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Technical Accuracy:** {eval_data.get('technical_accuracy', 'N/A')}")
                st.markdown(f"**Communication Quality:** {eval_data.get('communication_quality', 'N/A')}")
                st.markdown(f"**Depth of Understanding:** {eval_data.get('depth_of_understanding', 'N/A')}")
            with c2:
                st.markdown(f"**Clarity of Explanation:** {eval_data.get('clarity', 'N/A')}")
                st.markdown(f"**Industry Relevance:** {eval_data.get('industry_relevance', 'N/A')}")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Missing concepts & suggestions
            c_missing, c_suggest = st.columns(2)
            with c_missing:
                st.markdown("<div style='color: var(--error); font-weight:600; font-size:0.9rem; margin-bottom:6px;'>Missing Technical Concepts:</div>", unsafe_allow_html=True)
                missing = eval_data.get("missing_concepts", [])
                if missing:
                    for m in missing:
                        st.markdown(f"- {m}")
                else:
                    st.write("Excellent! Covered all core expected concepts.")
            with c_suggest:
                st.markdown("<div style='color: var(--warning); font-weight:600; font-size:0.9rem; margin-bottom:6px;'>Actionable Suggestions:</div>", unsafe_allow_html=True)
                sugs = eval_data.get("suggestions", [])
                if sugs:
                    for s in sugs:
                        st.markdown(f"- {s}")
                else:
                    st.write("Answer was highly structured.")
                    
            # Ideal Answer
            with st.expander("Show Model Answer Reference"):
                st.write(eval_data.get("ideal_answer", "No ideal answer available."))
        
    # Actions
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Back to Dashboard", key="feedback_btn_dash", use_container_width=True):
            # Clear cached answers to avoid taking space
            st.session_state.interview_answers = {}
            st.session_state.current_page = "dashboard"
            st.rerun()
            
    with col_b:
        if st.button("Try Another Mock Session", key="feedback_btn_mock_retry", use_container_width=True):
            st.session_state.interview_answers = {}
            st.session_state.current_page = "interview_session"
            st.rerun()
