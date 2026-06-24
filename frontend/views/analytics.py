"""Analytics visualization dashboard showing skill levels, score trends, and progress."""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from components.charts import (
    score_trend_chart,
    topic_performance_chart,
    weekly_progress_chart,
    skill_growth_chart,
    interview_type_chart
)
from components.forms import display_error, display_info
from components.ui import page_header, section_title

def render_analytics_page():
    """Render the Plotly analytics sheets for user review."""
    col_b1, col_b2 = st.columns([5, 1.2])
    with col_b1:
        st.markdown("<div style='font-size: 0.85rem; color: var(--text-muted); padding: 4px 0;'>Dashboard &nbsp;&gt;&nbsp; <b>Analytics</b></div>", unsafe_allow_html=True)
    with col_b2:
        if st.button("Dashboard", key="back_to_dash_top"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("<hr style='border-color: var(--border); margin: 5px 0 20px 0;'>", unsafe_allow_html=True)
    
    page_header("Performance Analytics", "Review score trends, topic performance, weekly progress, and interview mix.", "Analytics")
    
    # 1. Fetch data
    with st.spinner("Compiling performance statistics..."):
        dash_res = api_client.get_dashboard()
        analytics_res = api_client.get_analytics()
        history_res = api_client.get_history()
        
    if not dash_res.get("success") or not analytics_res.get("success"):
        display_error("Could not fetch analytics data. Please perform some mock sessions first.")
        return
        
    d_data = dash_res["data"]
    a_data = analytics_res["data"]
    
    trend = d_data.get("score_trend", [])
    topic_perf = a_data.get("topic_performance", [])
    weekly_prog = a_data.get("weekly_progress", [])
    skill_grow = a_data.get("skill_growth", [])
    sessions = history_res.get("data", []) if history_res.get("success") else []
    
    if not trend and not topic_perf:
        display_info("No mock interview analytics available yet. Go ahead and start a mock session.")
        return
        
    # Full Width Score Trend
    with st.container(border=True):
        section_title("Overall Score Trend")
        fig_trend = score_trend_chart(trend)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Two Columns: Topic Radar/Bar & Session Type Donut
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            section_title("Topic Performance")
            fig_topic = topic_performance_chart(topic_perf)
            st.plotly_chart(fig_topic, use_container_width=True)
    with c2:
        with st.container(border=True):
            section_title("Interview Type Distribution")
            fig_donut = interview_type_chart(sessions)
            st.plotly_chart(fig_donut, use_container_width=True)
        
    # Weekly progress & Skill growth
    with st.container(border=True):
        section_title("Weekly Average Progress")
        fig_weekly = weekly_progress_chart(weekly_prog)
        st.plotly_chart(fig_weekly, use_container_width=True)
    
    with st.container(border=True):
        section_title("Topic Specific Skill Growth")
        fig_growth = skill_growth_chart(skill_grow)
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # Detailed Table
    with st.container(border=True):
        section_title("Detailed Topic Analysis")
        if topic_perf:
            df_topic = pd.DataFrame(topic_perf)
            df_topic.columns = ["Topic / Skill Area", "Average Grade (/10)", "Questions Attempted"]
            st.dataframe(
                df_topic.style.background_gradient(cmap="Blues", subset=["Average Grade (/10)"]),
                hide_index=True,
                use_container_width=True
            )
        else:
            st.write("No topic analytics details available.")
