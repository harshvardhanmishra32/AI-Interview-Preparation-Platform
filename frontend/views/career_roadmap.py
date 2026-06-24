"""AI Career Roadmap Generator interface page."""
import streamlit as st
import textwrap
from utils.api_client import api_client
from components.forms import display_error, display_success, display_info
from components.ui import page_header, safe_text

def render_career_roadmap():
    """Render the career roadmap selector and output views."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Dashboard &nbsp;&gt;&nbsp; <b>Career Roadmap</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Dashboard", key="back_to_dash_top"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    
    page_header("AI Career Roadmap Generator", "Generate a personalized learning pathway from resume context and interview analytics.", "Roadmap")
    
    user = st.session_state.user
    default_role = user.get("target_role") or "Software Engineer"
    
    with st.container(border=True):
        st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; font-weight:600; color: var(--text);'>Configure Roadmap Target</h3>", unsafe_allow_html=True)
        
        target_role = st.text_input("Target Job Role", value=default_role)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        roadmap_data = st.session_state.get("cached_career_roadmap")
        
        if st.button("Generate Roadmap Path", key="roadmap_generate_submit"):
            with st.spinner("Analyzing resume structure and grading profiles to build roadmap..."):
                res = api_client.generate_roadmap(target_role=target_role if target_role.strip() else None)
                if res.get("success"):
                    roadmap_data = res["data"]
                    st.session_state.cached_career_roadmap = roadmap_data
                    display_success("Personalized career roadmap generated.")
                else:
                    err_msg = res.get("error")
                    if err_msg:
                        display_error(f"Failed to generate roadmap: {err_msg}")
                    else:
                        display_error("Failed to generate roadmap. Make sure you have uploaded a resume first.")
    
    # Display roadmap if available
    if roadmap_data:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='font-weight:600; color: var(--text);'>Pathway for {safe_text(target_role)} <span style='font-size:1rem; color: var(--primary);'>(Estimated Time: {safe_text(roadmap_data.get('timeline', '6 Months'))})</span></h2>", unsafe_allow_html=True)
        
        # Skill Gaps list
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--error);'>Identified Skill Gaps</h3>", unsafe_allow_html=True)
            gaps = roadmap_data.get("skill_gaps", [])
            if gaps:
                badges_html = "".join([f"<span class='badge badge-danger'>{g}</span>" for g in gaps])
                st.markdown(f"<div style='flex-wrap: wrap;'>{badges_html}</div>", unsafe_allow_html=True)
            else:
                st.write("No major gaps identified.")
        
        # Two columns: Learning path steps & Recommended Certifications
        col_l, col_r = st.columns([3, 2])
        with col_l:
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--primary);'>Learning Modules</h3>", unsafe_allow_html=True)
                
                learning_path = roadmap_data.get("learning_path", [])
                if learning_path:
                    for idx, step in enumerate(learning_path):
                        priority_str = str(step.get("priority") or "Medium").strip().title()
                        p_color = "var(--error)" if priority_str == "High" else ("var(--warning)" if priority_str == "Medium" else "var(--success)")
                        
                        html_content = textwrap.dedent(f"""
                            <div style='background: var(--bg); border: 1px solid var(--border); border-radius:6px; padding:12px; margin-bottom:12px;'>
                                <div style='display:flex; justify-content:space-between; align-items:center;'>
                                    <span style='font-weight:600; font-size:0.95rem; color: var(--text);'>{idx + 1}. {safe_text(step.get('skill'))}</span>
                                    <span class='badge' style='background-color: var(--primary-muted); color: {p_color}; border: 1px solid var(--border);'>{priority_str} Priority</span>
                                </div>
                                <div style='font-size:0.8rem; color: var(--text-muted); margin-top:4px;'>Material: <b>{safe_text(step.get('resource'))}</b></div>
                                <div style='font-size:0.8rem; color: var(--primary); margin-top:2px;'>Duration: <b>{safe_text(step.get('duration'))}</b></div>
                            </div>
                        """)
                        st.markdown(html_content, unsafe_allow_html=True)
                else:
                    st.write("No learning steps compiled.")
            
        with col_r:
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--primary);'>Recommended Certifications</h3>", unsafe_allow_html=True)
                certs = roadmap_data.get("recommended_certifications", [])
                if certs:
                    for c in certs:
                        st.markdown(f"<div style='margin-bottom:8px; color: var(--text-muted);'><b>{safe_text(c)}</b></div>", unsafe_allow_html=True)
                else:
                    st.write("No credentials suggested.")
            
            # Suggested Projects
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--success);'>Showcase Portfolio Projects</h3>", unsafe_allow_html=True)
                projs = roadmap_data.get("suggested_projects", [])
                if projs:
                    for p in projs:
                        skills_applied = "".join([f"<span class='badge badge-primary' style='font-size:0.7rem; padding:2px 6px;'>{safe_text(sk)}</span>" for sk in p.get("skills_practiced", [])])
                        html_content = textwrap.dedent(f"""
                            <div style='margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid var(--border);'>
                                <div style='font-weight:600; font-size:0.9rem; color: var(--text);'>{safe_text(p.get('title'))}</div>
                                <div style='font-size:0.8rem; color: var(--text-muted); margin-top:2px;'>{safe_text(p.get('description'))}</div>
                                <div style='margin-top:4px;'>{skills_applied}</div>
                            </div>
                        """)
                        st.markdown(html_content, unsafe_allow_html=True)
                else:
                    st.write("No project guides suggested.")
            
        # Career phases timeline list
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--primary);'>Milestones Roadmap Phases</h3>", unsafe_allow_html=True)
            phases = roadmap_data.get("career_roadmap", [])
            if phases:
                for ph in phases:
                    goals_list = "".join([f"<li>{safe_text(gl)}</li>" for gl in ph.get("goals", [])])
                    milestones_list = "".join([f"<li>{safe_text(ml)}</li>" for ml in ph.get("milestones", [])])
                    
                    html_content = textwrap.dedent(f"""
                        <div style='background: var(--bg); border: 1px solid var(--border); border-radius:6px; padding:16px; margin-bottom:12px;'>
                            <div style='display:flex; justify-content:space-between; align-items:center;'>
                                <span style='font-weight:700; font-size:1rem; color: var(--primary);'>{safe_text(ph.get('phase'))}</span>
                                <span style='font-size:0.85rem; color: var(--text-muted); font-weight:600;'>{safe_text(ph.get('duration'))}</span>
                            </div>
                            <div style='display:flex; gap:20px; margin-top:10px;'>
                                <div style='flex:1;'>
                                    <div style='font-size:0.8rem; color: var(--text-muted); font-weight:600; text-transform:uppercase;'>Focus Goals:</div>
                                    <ul style='font-size:0.85rem; color: var(--text-muted); padding-left:16px;'>{goals_list}</ul>
                                </div>
                                <div style='flex:1;'>
                                    <div style='font-size:0.8rem; color: var(--text-muted); font-weight:600; text-transform:uppercase;'>Tracking Milestones:</div>
                                    <ul style='font-size:0.85rem; color: var(--text-muted); padding-left:16px;'>{milestones_list}</ul>
                                </div>
                            </div>
                        </div>
                    """)
                    st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.write("No phases detail mapped.")
        
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        display_info("Provide a target role above and click 'Generate Roadmap Path' to compile your visual learning timeline.")
