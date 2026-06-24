"""GitHub Profile Analyzer page view."""
import streamlit as st
import plotly.express as px
from utils.api_client import api_client
from components.forms import display_error, display_success, display_info
from components.ui import page_header, safe_text

def render_github_analyzer():
    """Render the GitHub profile analyzer panel and visualizations."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Dashboard &nbsp;&gt;&nbsp; <b>GitHub Analyzer</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Dashboard", key="back_to_dash_top"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    
    page_header("GitHub Profile Analyzer", "Analyze public repositories, language distribution, portfolio signals, and project-specific interview questions.", "Portfolio")
    
    with st.container(border=True):
        st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; font-weight:600; color: var(--text);'>Enter Profile Link</h3>", unsafe_allow_html=True)
        
        github_url = st.text_input("GitHub URL", placeholder="https://github.com/your-username")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        analysis_data = st.session_state.get("cached_github_analysis")
        
        if st.button("Analyze GitHub Profile", key="github_analyze_submit"):
            if not github_url.strip():
                display_error("Please enter a valid GitHub profile URL.")
            else:
                with st.spinner("Connecting to GitHub API and analyzing repositories..."):
                    res = api_client.analyze_github(github_url)
                    if res.get("success"):
                        analysis_data = res["data"]
                        st.session_state.cached_github_analysis = analysis_data
                        display_success("GitHub profile analysis completed.")
                    else:
                        display_error(res.get("error", "Failed to analyze GitHub profile. Verify username matches a public account."))
    
    if analysis_data:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='font-weight:600; color: var(--text);'>Portfolio Report: {safe_text(analysis_data.get('username'))}</h2>", unsafe_allow_html=True)
        
        # Contribution text summary
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--primary);'>Contribution Summary</h3>", unsafe_allow_html=True)
            st.write(analysis_data.get("contribution_summary"))
        
        # Columns: Repos list & Language Donut chart
        col_l, col_r = st.columns([3, 2])
        
        with col_l:
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--primary);'>Key Repositories</h3>", unsafe_allow_html=True)
                
                repos = analysis_data.get("repositories", [])
                if repos:
                    for r in repos:
                        st.markdown(
                            f"""
                            <div style='background: var(--bg); border: 1px solid var(--border); border-radius:6px; padding:12px; margin-bottom:10px;'>
                                <div style='display:flex; justify-content:space-between; align-items:center;'>
                                    <span style='font-weight:600; font-size:0.95rem; color: var(--text);'>{safe_text(r.get('name'))}</span>
                                    <span style='font-size:0.8rem; color: var(--primary); font-weight:500;'>{safe_text(r.get('language') or 'Text')}</span>
                                </div>
                                <div style='font-size:0.8rem; color: var(--text-muted); margin-top:2px;'>{safe_text(r.get('description') or 'No description provided.')}</div>
                                <div style='font-size:0.75rem; color: var(--text-muted); margin-top:4px;'>{safe_text(r.get('stars'))} stars | {safe_text(r.get('forks'))} forks</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.write("No public repositories found.")
            
        with col_r:
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--primary);'>Language Share</h3>", unsafe_allow_html=True)
                
                langs = analysis_data.get("languages", {})
                if langs:
                    # Plotly donut chart
                    lang_df = [{"Language": k, "Count": v} for k, v in langs.items()]
                    fig = px.pie(
                        lang_df,
                        values="Count",
                        names="Language",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    
                    theme = st.session_state.get("theme_preference", "Light")
                    chart_template = "plotly_dark" if theme == "Dark" else "plotly_white"
                    
                    fig.update_layout(
                        template=chart_template,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=240,
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No language metadata parsed.")
            
            # Skill Assessment
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--success);'>Skill Assessment</h3>", unsafe_allow_html=True)
                assess = analysis_data.get("skill_assessment", [])
                if assess:
                    for as_item in assess:
                        st.markdown(f"<div style='color: var(--text-muted); margin-bottom: 4px;'>{safe_text(as_item)}</div>", unsafe_allow_html=True)
                else:
                    st.write("No assessment details available.")
            
        # Project specific questions
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--warning);'>Project-Specific Mock Questions</h3>", unsafe_allow_html=True)
            questions = analysis_data.get("project_questions", [])
            if questions:
                for idx, q in enumerate(questions):
                    concepts_badges = "".join([f"<span class='badge badge-primary' style='font-size:0.75rem; padding:2px 6px;'>{safe_text(c)}</span>" for c in q.get("expected_concepts", [])])
                    st.markdown(
                        f"""
                        <div style='background: var(--bg); border: 1px solid var(--border); border-radius:6px; padding:16px; margin-bottom:12px;'>
                            <div style='font-size:0.8rem; color: var(--primary); font-weight:600; text-transform:uppercase;'>Question {idx + 1} - Project: {safe_text(q.get('project_name'))}</div>
                            <div style='font-weight:600; font-size:0.95rem; color: var(--text); margin-top:4px;'>{safe_text(q.get('question'))}</div>
                            <div style='margin-top:6px;'>{concepts_badges}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.write("No project specific questions compiled.")
        
        # Recommendations
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--primary);'>Portfolio Recommendations</h3>", unsafe_allow_html=True)
            recom = analysis_data.get("recommendations", [])
            if recom:
                for rec in recom:
                    st.markdown(f"<div style='color: var(--text-muted); margin-bottom: 4px;'>{safe_text(rec)}</div>", unsafe_allow_html=True)
            else:
                st.write("No recommendations compiled.")
        
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        display_info("Input a GitHub profile URL above to parse your projects and generate repository specific questions.")
