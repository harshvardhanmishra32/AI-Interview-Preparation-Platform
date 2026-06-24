"""Portfolio About Me page for Harshvardhan Mishra, tailored for recruiters."""
import streamlit as st
from components.ui import page_header

def render_about_me_page():
    """Render the premium portfolio showcase page."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Home &nbsp;&gt;&nbsp; <b>About Me</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Back to Home", key="back_home_top"):
            st.session_state.current_page = "landing"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    # Glassy background styling overrides
    st.markdown(
        """
        <style>
        .profile-header {
            display: flex;
            align-items: center;
            gap: 24px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .profile-pic-container {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--success) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3.5rem;
            color: #ffffff;
            box-shadow: var(--shadow);
            border: 3px solid var(--border);
        }
        .role-badge {
            background: var(--primary-muted);
            color: var(--primary);
            border: 1px solid var(--border);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin-top: 6px;
        }
        .timeline {
            border-left: 2px solid var(--border);
            margin: 15px 0 15px 15px;
            padding-left: 20px;
            position: relative;
        }
        .timeline-item {
            margin-bottom: 25px;
            position: relative;
        }
        .timeline-item::before {
            content: "";
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--primary);
            border: 2px solid var(--bg);
            position: absolute;
            left: -27px;
            top: 5px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }
        .timeline-item.edu::before {
            background: var(--success);
        }
        .timeline-item:hover::before {
            transform: scale(1.3);
        }
        .timeline-date {
            font-size: 0.8rem;
            color: var(--primary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .timeline-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
            margin: 0;
        }
        .timeline-subtitle {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin: 2px 0 8px 0;
            font-weight: 500;
        }
        .timeline-description {
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.5;
        }
        .skill-group {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }
        .skill-group-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 10px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 6px;
        }
        .social-link {
            text-decoration: none;
            color: var(--text-muted);
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.9rem;
            padding: 8px 16px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        .social-link:hover {
            color: var(--primary) !important;
            border-color: var(--primary);
            background: var(--primary-muted);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    page_header("About Me", "Professional portfolio summary, education, skills, achievements, and contact details.", "Portfolio")

    # PROFILE SUMMARY BLOCK
    with st.container(border=True):
        st.markdown(
            """
            <div class="profile-header">
                <div class="profile-pic-container">HM</div>
                <div>
                    <h2 style='margin: 0; font-size: 2rem; font-weight: 700; color: var(--text);'>Harshvardhan Mishra</h2>
                    <div class="role-badge">B.Tech CSE Student | AI/ML Enthusiast | Python Developer</div>
                    <div style='margin-top: 10px; font-size: 0.9rem; color: var(--text-muted);'>
                        Lucknow, India &nbsp;•&nbsp; <a href="mailto:harshvardhanmishra31@gmail.com" style="color: var(--primary); text-decoration: none;">harshvardhanmishra31@gmail.com</a>
                    </div>
                </div>
            </div>
            
            <p style="font-size: 0.95rem; line-height: 1.6; color: var(--text-muted);">
                I am a passionate Computer Science and Engineering student at Babu Banarasi Das Northern India Institute of Technology (BBDNIIT), Lucknow. With a solid foundation in Python development and a deep curiosity for Artificial Intelligence and Machine Learning, I build intelligent tools that bridge academic logic and real-world utility.
            </p>
            <p style="font-size: 0.95rem; line-height: 1.6; color: var(--text-muted); margin-bottom: 0;">
                As a technical coordinator and society leader, I thrive in collaborative environments, managing hackathons and developer communities to foster digital innovation.
            </p>
            """,
            unsafe_allow_html=True
        )

    # TWO COLUMNS Layout
    col_l, col_r = st.columns([3, 2])

    with col_l:
        # TIMELINE SECTION
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--primary);'>Professional & Academic Journey</h3>", unsafe_allow_html=True)
            
            st.markdown(
                """
                <div class="timeline">
                    <!-- Milestone 1 -->
                    <div class="timeline-item edu">
                        <div class="timeline-date">2022 - 2026 (Expected)</div>
                        <div class="timeline-title">B.Tech in Computer Science & Engineering</div>
                        <div class="timeline-subtitle">Babu Banarasi Das Northern India Institute of Technology (BBDNIIT), Lucknow</div>
                        <div class="timeline-description">
                            Focused on Data Structures, Algorithms, Software Engineering, Database Systems, and Artificial Intelligence models. Maintained a strong academic record while coordinating campus technical initiatives.
                        </div>
                    </div>
                    <!-- Milestone 2 -->
                    <div class="timeline-item">
                        <div class="timeline-date">2024 - Present</div>
                        <div class="timeline-title">Student Technical Coordinator</div>
                        <div class="timeline-subtitle">Abhikalp Technical Society</div>
                        <div class="timeline-description">
                            Managed coding workshops, project design labs, and hackathons. Structured technical frameworks for student projects and mentored juniors on programming fundamentals.
                        </div>
                    </div>
                    <!-- Milestone 3 -->
                    <div class="timeline-item">
                        <div class="timeline-date">2024 - 2025</div>
                        <div class="timeline-title">Student Chapter Co-Lead</div>
                        <div class="timeline-subtitle">GeeksforGeeks (GFG) Student Chapter, BBDNIIT</div>
                        <div class="timeline-description">
                            Organized weekly coding challenges, programming guest lectures, and standard DSA bootcamps, driving candidate participation up by over 40% across campus.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_r:
        # SKILLS SECTION
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--success);'>Technical Tooling</h3>", unsafe_allow_html=True)
            
            # Group 1
            st.markdown(
                """
                <div class="skill-group">
                    <div class="skill-group-title">Languages & Frameworks</div>
                    <span class="badge badge-primary">Python</span>
                    <span class="badge badge-primary">C/C++</span>
                    <span class="badge badge-primary">FastAPI</span>
                    <span class="badge badge-primary">Streamlit</span>
                    <span class="badge badge-primary">SQL</span>
                    <span class="badge badge-primary">HTML5/CSS3</span>
                </div>
                
                <div class="skill-group">
                    <div class="skill-group-title">Machine Learning & AI</div>
                    <span class="badge badge-success">Google Gemini API</span>
                    <span class="badge badge-success">Scikit-Learn</span>
                    <span class="badge badge-success">Pandas</span>
                    <span class="badge badge-success">NumPy</span>
                    <span class="badge badge-success">ChromaDB (Vector DB)</span>
                    <span class="badge badge-success">NLP</span>
                </div>
                
                <div class="skill-group">
                    <div class="skill-group-title">Tools & Engineering</div>
                    <span class="badge badge-warning">Git & GitHub</span>
                    <span class="badge badge-warning">REST APIs</span>
                    <span class="badge badge-warning">SQLite</span>
                    <span class="badge badge-warning">JSON Processing</span>
                    <span class="badge badge-warning">Object-Oriented Design</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # CONTACT & RESUME DOWNLOAD
        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 16px 0; font-size:1.1rem; color: var(--warning);'>Contact & Credentials</h3>", unsafe_allow_html=True)
            
            # Download Resume Button
            # Simulated PDF download content (using base resume placeholder)
            resume_data = "Harshvardhan Mishra - Software Engineer & AI/ML Developer - email: harshvardhanmishra31@gmail.com"
            st.download_button(
                label="Download Harshvardhan's Resume",
                data=resume_data.encode("utf-8"),
                file_name="harshvardhan_mishra_resume.txt",
                mime="text/plain",
                key="resume_downloader_btn"
            )
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            
            # Custom styled social links
            st.markdown(
                """
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <a href="mailto:harshvardhanmishra31@gmail.com" class="social-link">
                        <span>Email</span> harshvardhanmishra31@gmail.com
                    </a>
                    <a href="https://github.com" target="_blank" class="social-link">
                        <span>GitHub</span> Portfolio Profile
                    </a>
                    <a href="https://linkedin.com" target="_blank" class="social-link">
                        <span>LinkedIn</span> Professional Profile
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
