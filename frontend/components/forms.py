"""Form validation and status messages styled for application consistency."""
import streamlit as st
from components.ui import safe_text

def display_error(message: str):
    """Render a styled critical/error message block."""
    st.markdown(
        f"""
        <div style='
            background-color: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.25);
            border-radius: 8px;
            padding: 12px 16px;
            color: var(--error);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 16px;
        '>
            {safe_text(message)}
        </div>
        """,
        unsafe_allow_html=True
    )

def display_success(message: str):
    """Render a styled success feedback block."""
    st.markdown(
        f"""
        <div style='
            background-color: rgba(34, 197, 94, 0.08);
            border: 1px solid rgba(34, 197, 94, 0.25);
            border-radius: 8px;
            padding: 12px 16px;
            color: var(--success);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 16px;
        '>
            {safe_text(message)}
        </div>
        """,
        unsafe_allow_html=True
    )

def display_info(message: str):
    """Render an informational tip or message block."""
    st.markdown(
        f"""
        <div style='
            background-color: var(--primary-muted);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px 16px;
            color: var(--primary);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 16px;
        '>
            {safe_text(message)}
        </div>
        """,
        unsafe_allow_html=True
    )
