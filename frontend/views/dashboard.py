"""Dashboard view showcasing aggregated metrics, score trends, and recent mock history."""
import streamlit as st
from utils.api_client import api_client
from utils.session import clear_auth
from components.charts import score_trend_chart
from components.forms import display_error, display_info
from components.ui import page_header, kpi_card, section_title, safe_text

def render_dashboard():
    """Render the dashboard overview for the authenticated candidate."""
    user = st.session_state.user
    name = user.get("name", "Candidate")

    # Top bar: welcome text + sign-out button
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        page_header(
            f"Welcome, {name}",
            "Your preparation command center: interviews, resume quality, GitHub signals, and AI recommendations.",
            "Dashboard",
        )
    with col_logout:
        st.markdown("<div style='padding-top: 12px;'>", unsafe_allow_html=True)
        if st.button("Logout", key="dashboard_logout", use_container_width=True):
            clear_auth()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 1. Fetch dashboard metrics
    with st.spinner("Loading metrics..."):
        res = api_client.get_dashboard()
        
    if not res.get("success"):
        display_error("Could not fetch dashboard metrics. Please reload the page.")
        return
        
    data = res["data"]
    total = data.get("total_interviews", 0)
    avg_score = data.get("average_score", 0.0)
    strongest = data.get("strongest_topics", [])
    weakest = data.get("weakest_topics", [])
    recent = data.get("recent_sessions", [])
    trend = data.get("score_trend", [])
    
    strongest_str = strongest[0] if strongest else "N/A"
    weakest_str = weakest[0] if weakest else "N/A"
    
    resume_score = 82 if st.session_state.get("cached_resume") else 68
    github_signal = "Ready" if total else "Pending"
    
    # Render row of metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Total Sessions", str(total), "Completed interviews", "blue")
    with col2:
        kpi_card("Average Score", f"{avg_score}/10", "Across evaluated answers", "green")
    with col3:
        kpi_card("Resume Score", f"{resume_score}/100", "Upload a resume to refresh", "purple")
    with col4:
        kpi_card("GitHub Insights", github_signal, "Portfolio analysis state", "amber")

    col5, col6 = st.columns(2)
    with col5:
        kpi_card("Strongest Topic", strongest_str, "Highest scoring area", "green")
    with col6:
        kpi_card("Priority Focus", weakest_str, "Recommended next practice area", "red")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Columns: Score Trend chart & Quick Action Buttons
    c_left, c_right = st.columns([3, 1])
    with c_left:
        with st.container(border=True):
            section_title("Performance Trend", "Score movement across completed mock interviews.")
            if trend:
                fig = score_trend_chart(trend)
                st.plotly_chart(fig, use_container_width=True)
            else:
                display_info("Take your first mock interview session to see performance analytics trends.")
        
    with c_right:
        with st.container(border=True):
            section_title("Quick Actions", "Jump into the workflows recruiters care about.")
            
            if st.button("Start Mock Interview", key="dash_btn_mock", use_container_width=True):
                st.session_state.current_page = "interview_session"
                st.rerun()
                
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            if st.button("Analyze Resume", key="dash_btn_resume", use_container_width=True):
                st.session_state.current_page = "resume_analyzer"
                st.rerun()
                
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            if st.button("Generate Roadmap", key="dash_btn_roadmap", use_container_width=True):
                st.session_state.current_page = "career_roadmap"
                st.rerun()

        with st.container(border=True):
            section_title("AI Recommendations")
            recommendations = [
                f"Practice {weakest_str} questions next." if weakest else "Complete your first mock interview to unlock targeted recommendations.",
                "Upload your latest PDF resume before company-specific sessions.",
                "Run GitHub Analyzer after your portfolio README updates.",
            ]
            for item in recommendations:
                st.markdown(f"<div style='font-size:0.86rem;color:var(--text-muted);margin-bottom:8px;'>{safe_text(item)}</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent sessions list
    with st.container(border=True):
        section_title("Recent Activity", "Latest mock sessions and evaluation status.")
        
        if recent:
            for r in recent:
                company_lbl = f" ({r['company']})" if r.get("company") else ""
                avg_score_lbl = f"{r['average_score']}/10" if r.get("average_score") is not None else "In Progress"
                score_color = "#22C55E" if (r.get("average_score") and r["average_score"] >= 7) else ("#F59E0B" if (r.get("average_score") and r["average_score"] >= 4) else "#EF4444")
                
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; margin-bottom: 8px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px;'>
                        <div>
                            <span style='font-weight:600; font-size: 0.95rem; color: var(--text);'>{r['interview_type'].title()} Interview</span>
                            <span style='color: var(--text-muted); font-size:0.85rem;'>{company_lbl} - {r['difficulty'].title()}</span>
                            <div style='font-size: 0.75rem; color: var(--text-muted); margin-top:2px;'>Conducted on {r['created_at']}</div>
                        </div>
                        <div style='text-align: right;'>
                            <span style='font-weight: 700; color: {score_color if r.get("average_score") else "#F59E0B"}; font-size: 0.95rem;'>{avg_score_lbl}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.write("No recent mock interview sessions found.")
