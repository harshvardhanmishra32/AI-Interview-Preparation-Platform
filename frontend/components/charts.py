"""Plotly visualization component helper functions styled for dark theme integration."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def score_trend_chart(data: list) -> go.Figure:
    """Create a styled line chart showing average score progression over time."""
    if not data:
        fig = go.Figure()
        fig.add_annotation(text="No interview data available yet.", showarrow=False, font=dict(color="#64748B"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig
        
    df = pd.DataFrame(data)
    # Ensure keys exist
    if "date" not in df.columns or "average_score" not in df.columns:
        return go.Figure()
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["average_score"],
        mode="lines+markers",
        name="Score",
        line=dict(color="#2563EB", width=3),
        marker=dict(color="#2563EB", size=7),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.10)"
    ))
    
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(color="#64748B"),
        xaxis=dict(showgrid=False, title="Interview Date"),
        yaxis=dict(gridcolor="rgba(148,163,184,0.18)", title="Score out of 10", range=[0, 10.5]),
        height=300
    )
    return fig

def topic_performance_chart(data: list) -> go.Figure:
    """Create a radar or bar chart showing performance score per topic area."""
    if not data:
        fig = go.Figure()
        fig.add_annotation(text="No topic data available.", showarrow=False, font=dict(color="#64748B"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig
        
    df = pd.DataFrame(data)
    
    # If we have very few topics, a horizontal bar chart looks much cleaner than radar
    if len(df) < 3:
        fig = px.bar(
            df,
            y="topic",
            x="average_score",
            orientation="h",
            color="average_score",
            color_continuous_scale=["#EF4444", "#F59E0B", "#22C55E"],
            range_x=[0, 10]
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=10, b=20),
            font=dict(color="#64748B"),
            xaxis=dict(gridcolor="rgba(148,163,184,0.18)", title="Score"),
            yaxis=dict(showgrid=False, title=""),
            height=250
        )
        return fig
        
    # Radar chart for 3+ topics
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df["average_score"],
        theta=df["topic"],
        fill="toself",
        fillcolor="rgba(37, 99, 235, 0.12)",
        line=dict(color="#2563EB", width=2),
        marker=dict(color="#6366F1")
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(148,163,184,0.18)"),
            angularaxis=dict(gridcolor="rgba(148,163,184,0.18)")
        ),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=30, b=30),
        showlegend=False,
        height=280
    )
    return fig

def weekly_progress_chart(data: list) -> go.Figure:
    """Create bar chart demonstrating average scores per week."""
    if not data:
        fig = go.Figure()
        fig.add_annotation(text="No weekly data available.", showarrow=False, font=dict(color="#64748B"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig
        
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x="week",
        y="average_score",
        text="average_score",
        color="interview_count",
        color_continuous_scale=["#DBEAFE", "#2563EB"],
        labels={"average_score": "Avg Score", "week": "Week Start", "interview_count": "Sessions"}
    )
    
    fig.update_traces(textposition="outside", marker_line_color="rgba(255,255,255,0.05)", marker_line_width=1.5)
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=False),
        font=dict(color="#64748B"),
        yaxis=dict(gridcolor="rgba(148,163,184,0.18)", range=[0, 11]),
        height=280
    )
    return fig

def skill_growth_chart(data: list) -> go.Figure:
    """Create line chart showing score growth over time per skill/topic."""
    if not data:
        fig = go.Figure()
        fig.add_annotation(text="No growth data available.", showarrow=False, font=dict(color="#64748B"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig
        
    df = pd.DataFrame(data)
    fig = px.line(
        df,
        x="week",
        y="average_score",
        color="topic",
        markers=True,
        line_shape="linear",
        color_discrete_sequence=["#2563EB", "#22C55E", "#F59E0B", "#6366F1", "#EF4444"]
    )
    
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=False),
        font=dict(color="#64748B"),
        yaxis=dict(gridcolor="rgba(148,163,184,0.18)", range=[0, 10.5]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=300
    )
    return fig

def interview_type_chart(sessions: list) -> go.Figure:
    """Create a pie/donut chart representing interview types distribution."""
    if not sessions:
        fig = go.Figure()
        fig.add_annotation(text="No history.", showarrow=False)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig
        
    df = pd.DataFrame(sessions)
    if "interview_type" not in df.columns:
        return go.Figure()
        
    type_counts = df["interview_type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    
    # Capitalize types for display
    type_counts["Type"] = type_counts["Type"].apply(lambda x: x.replace("_", " ").title())
    
    fig = px.pie(
        type_counts,
        values="Count",
        names="Type",
        hole=0.4,
        color_discrete_sequence=["#2563EB", "#22C55E", "#F59E0B", "#6366F1"]
    )
    
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.9),
        height=250
    )
    return fig
