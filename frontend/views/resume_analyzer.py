"""Resume parser and analyzer interface page."""
import streamlit as st
from utils.api_client import api_client
from components.forms import display_error, display_success, display_info
from components.ui import page_header, section_title, safe_text, badge


def _as_list(value) -> list:
    """Normalize nullable API list fields for stable rendering."""
    if isinstance(value, list):
        return value
    if value:
        return [str(value)]
    return []


def _analysis_overview(resume: dict) -> None:
    """Render a compact analysis summary immediately after upload/load."""
    skills = _as_list(resume.get("skills"))
    projects = _as_list(resume.get("projects"))
    gaps = _as_list(resume.get("missing_skills"))
    suggestions = _as_list(resume.get("suggestions"))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Skills Found", len(skills))
    with c2:
        st.metric("Projects Found", len(projects))
    with c3:
        st.metric("Skill Gaps", len(gaps))
    with c4:
        st.metric("Suggestions", len(suggestions))


def render_resume_analyzer():
    """Render the resume uploading and parser analysis workspace."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Dashboard &nbsp;&gt;&nbsp; <b>Resume Analyzer</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Dashboard", key="back_to_dash_top"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    
    page_header("Resume Analyzer", "Upload a PDF resume to extract skills, project scope, experience, and AI improvement suggestions.", "Preparation Tool")
    
    # 1. Fetch existing resume analysis, using session state first so upload results
    # survive Streamlit reruns and are rendered immediately after processing.
    existing_resume = st.session_state.get("cached_resume")
    if existing_resume is None:
        with st.spinner("Checking for existing resume..."):
            res = api_client.get_resume()
            if res.get("success"):
                existing_resume = res["data"]
                st.session_state.cached_resume = existing_resume
    upload_success_msg = st.session_state.pop("resume_upload_success", None)
            
    # File uploader container
    with st.container(border=True):
        section_title("Upload PDF Resume", "Text-based PDFs up to 10MB are supported.")
        
        uploaded_file = st.file_uploader("Select PDF File (max 10MB)", type=["pdf"], key="resume_pdf_uploader")
        
        if uploaded_file is not None:
            if st.button("Process & Analyze Resume", key="resume_process_submit", use_container_width=True):
                file_bytes = uploaded_file.read()
                if len(file_bytes) > 10 * 1024 * 1024:
                    display_error("Resume file is too large. Maximum allowed size is 10MB.")
                else:
                    with st.spinner("Parsing resume text and preparing analysis..."):
                        upload_res = api_client.upload_resume(file_bytes, uploaded_file.name)
                    
                        if upload_res.get("success"):
                            existing_resume = upload_res["data"]
                            st.session_state.cached_resume = existing_resume
                            st.session_state.resume_upload_success = "Resume processed and analyzed successfully. Analysis is ready below."
                            st.rerun()
                        else:
                            display_error(upload_res.get("error", "Failed to analyze resume."))
    
    # Display details if resume is loaded
    if existing_resume:
        st.markdown("<br>", unsafe_allow_html=True)
        if upload_success_msg:
            display_success(upload_success_msg)
        
        st.markdown("<h2 style='font-weight:600; color: var(--text);'>Resume Analysis Profile</h2>", unsafe_allow_html=True)
        _analysis_overview(existing_resume)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Two columns layout: Summary & Strengths/Suggestions
        col_l, col_r = st.columns([3, 2])
        
        with col_l:
            # Summary
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--primary);'>Professional Summary</h3>", unsafe_allow_html=True)
                st.write(existing_resume.get("summary", "No summary available."))
            
            # Skills tags
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--primary);'>Extracted Technical Skills</h3>", unsafe_allow_html=True)
                skills = _as_list(existing_resume.get("skills"))
                if skills:
                    badges_html = "".join([badge(s, "primary") for s in skills])
                    st.markdown(f"<div style='flex-wrap: wrap;'>{badges_html}</div>", unsafe_allow_html=True)
                else:
                    st.write("No skills extracted.")
            
            # Projects & Experience
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--primary);'>Experience & Projects</h3>", unsafe_allow_html=True)
                
                # Experience
                st.markdown("<h4 style='font-size:0.95rem; font-weight:600; color: var(--text);'>Work History</h4>", unsafe_allow_html=True)
                experience = _as_list(existing_resume.get("experience"))
                if experience:
                    for exp in experience:
                        st.markdown(f"- {exp}")
                else:
                    st.write("No work experience details parsed.")
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Projects
                st.markdown("<h4 style='font-size:0.95rem; font-weight:600; color: var(--text);'>Projects</h4>", unsafe_allow_html=True)
                projects = _as_list(existing_resume.get("projects"))
                if projects:
                    for proj in projects:
                        st.markdown(f"- {proj}")
                else:
                    st.write("No projects details parsed.")
            
        with col_r:
            # Strengths
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--success);'>Resume Strengths</h3>", unsafe_allow_html=True)
                strengths = _as_list(existing_resume.get("strengths"))
                if strengths:
                    for strg in strengths:
                        st.markdown(f"<div style='margin-bottom:6px; color: var(--text-muted);'>{safe_text(strg)}</div>", unsafe_allow_html=True)
                else:
                    st.write("No strengths listed.")
            
            # Missing Skills
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--error);'>Potential Skill Gaps</h3>", unsafe_allow_html=True)
                missing = _as_list(existing_resume.get("missing_skills"))
                if missing:
                    badges_html = "".join([badge(m, "danger") for m in missing])
                    st.markdown(f"<div style='flex-wrap: wrap;'>{badges_html}</div>", unsafe_allow_html=True)
                else:
                    st.write("No skill gaps flagged.")
            
            # Improvement Suggestions
            with st.container(border=True):
                st.markdown("<h3 style='margin:0 0 12px 0; font-size:1.1rem; color: var(--warning);'>Suggestions for Improvement</h3>", unsafe_allow_html=True)
                suggestions = _as_list(existing_resume.get("suggestions"))
                if suggestions:
                    for sug in suggestions:
                        st.markdown(f"<div style='margin-bottom:6px; color: var(--text-muted);'>{safe_text(sug)}</div>", unsafe_allow_html=True)
                else:
                    st.write("No suggestions available.")
            
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        display_info("Please upload your PDF resume to initialize your candidate profile and get started.")
