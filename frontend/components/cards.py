"""Premium card components styled with theme CSS variables for light/dark compatibility."""
import streamlit as st
from components.ui import safe_text

def metric_card(title: str, value: str, icon: str, color: str = "#4F8CFF"):
    """Render a premium dashboard metric card with dynamic styling."""
    st.markdown(
        f"""
        <div style='
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-top: 1.5px solid var(--border);
            border-left: 3px solid {color};
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 12px;
            box-shadow: var(--shadow);
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <div style='font-size: 14px; color: var(--text-muted); font-weight: 500;'>{safe_text(title)}</div>
                    <div style='font-size: 28px; font-weight: 700; color: var(--text); margin-top: 4px; letter-spacing: 0;'>{safe_text(value)}</div>
                </div>
                <div style='font-size: 1rem; color: {color}; opacity: 0.9; font-weight:700;'>{safe_text(icon)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def info_card(title: str, content: str, icon: str = "ℹ️"):
    """Render an informational card for showcasing guidelines or text content."""
    st.markdown(
        f"""
        <div style='
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-top: 1.5px solid var(--border);
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: var(--shadow);
        '>
            <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                <span style='font-size: 1.1rem; margin-right: 8px;'>{safe_text(icon)}</span>
                <span style='font-weight: 600; font-size: 16px; color: var(--text);'>{safe_text(title)}</span>
            </div>
            <div style='font-size: 14px; color: var(--text-muted); line-height: 1.6;'>{safe_text(content)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def score_card(score: float, label: str = "Overall Score"):
    """Render a visual representation of a score out of 10."""
    color = "#22C55E" if score >= 7 else ("#F59E0B" if score >= 4 else "#EF4444")
    st.markdown(
        f"""
        <div style='
            text-align: center;
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-top: 2.5px solid {color};
            border-radius: 50%;
            width: 140px;
            height: 140px;
            margin: 0 auto 16px auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: var(--shadow);
        '>
            <div style='font-size: 32px; font-weight: 700; color: var(--text); letter-spacing: 0;'>{safe_text(score)}</div>
            <div style='font-size: 12px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; margin-top: 2px;'>{safe_text(label)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def feature_card(title: str, description: str, icon: str):
    """Render feature card for landing welcome page."""
    st.markdown(
        f"""
        <div style='
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-top: 1.5px solid var(--border);
            border-radius: 6px;
            padding: 24px;
            height: 100%;
            box-shadow: var(--shadow);
            transition: all 250ms ease;
        '>
            <div style='font-size: 1rem; margin-bottom: 12px; color: var(--primary); font-weight:700;'>{safe_text(icon)}</div>
            <div style='font-weight: 600; font-size: 18px; color: var(--text); margin-bottom: 8px;'>{safe_text(title)}</div>
            <div style='font-size: 14px; color: var(--text-muted); line-height: 1.6;'>{safe_text(description)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
