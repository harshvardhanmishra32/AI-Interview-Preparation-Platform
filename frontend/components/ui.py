"""Shared Streamlit UI helpers for the PREPAI product shell."""
from __future__ import annotations

from html import escape
import streamlit as st


def safe_text(value) -> str:
    """Escape text before placing it inside custom HTML."""
    return escape("" if value is None else str(value))


def breadcrumb(*items: str) -> None:
    """Render a compact breadcrumb trail."""
    trail = " / ".join(
        f"<span>{safe_text(item)}</span>" if idx < len(items) - 1 else f"<strong>{safe_text(item)}</strong>"
        for idx, item in enumerate(items)
    )
    st.markdown(f"<div class='app-breadcrumb'>{trail}</div>", unsafe_allow_html=True)


def page_header(title: str, subtitle: str | None = None, eyebrow: str | None = None) -> None:
    """Render a consistent enterprise page header."""
    eyebrow_html = f"<div class='page-eyebrow'>{safe_text(eyebrow)}</div>" if eyebrow else ""
    subtitle_html = f"<p>{safe_text(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <section class="page-header">
            {eyebrow_html}
            <h1>{safe_text(title)}</h1>
            {subtitle_html}
        </section>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, detail: str = "", tone: str = "blue") -> None:
    """Render a compact KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card kpi-{safe_text(tone)}">
            <div class="kpi-label">{safe_text(label)}</div>
            <div class="kpi-value">{safe_text(value)}</div>
            <div class="kpi-sub">{safe_text(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str | None = None) -> None:
    """Render a section title for framed Streamlit containers."""
    sub = f"<p>{safe_text(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"<div class='section-title'><h3>{safe_text(title)}</h3>{sub}</div>",
        unsafe_allow_html=True,
    )


def badge(label: str, tone: str = "blue") -> str:
    """Return a badge HTML string."""
    return f"<span class='badge badge-{safe_text(tone)}'>{safe_text(label)}</span>"
