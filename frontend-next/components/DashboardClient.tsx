"use client";

import { useEffect, useState } from "react";
import { apiRequest, DashboardData } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

export function DashboardClient() {
  const { token, user } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    apiRequest<DashboardData>("/api/analytics/dashboard", {}, token).then((result) => {
      if (result.ok) setData(result.data);
      else setError(result.error);
    });
  }, [token]);

  const metrics = [
    ["Total Sessions", data?.total_interviews ?? 0],
    ["Average Score", `${(data?.average_score ?? 0).toFixed(1)}/10`],
    ["Strong Topics", data?.strongest_topics?.[0] || "Pending"],
    ["Focus Area", data?.weakest_topics?.[0] || "Pending"]
  ];

  return (
    <AppShell>
      <PageHeader
        eyebrow="Dashboard"
        title={`Welcome, ${user?.name || "Candidate"}`}
        description="Your command center for interview sessions, resume signal, portfolio readiness, and AI recommendations."
      />
      {error ? <div className="alert error">{error}</div> : null}
      <div className="metric-grid">
        {metrics.map(([label, value]) => (
          <div className="card" key={label}>
            <div className="metric-label">{label}</div>
            <div className="metric-value">{value}</div>
          </div>
        ))}
      </div>
      <div className="cards-grid">
        <section className="card">
          <h3>Score Trend</h3>
          <div className="stack">
            {(data?.score_trend || []).slice(-5).map((entry) => (
              <div key={entry.date}>
                <div className="toolbar" style={{ marginBottom: 6 }}>
                  <span>{entry.date}</span>
                  <strong>{entry.average_score.toFixed(1)}</strong>
                </div>
                <div className="bar">
                  <span style={{ width: `${Math.min(100, entry.average_score * 10)}%` }} />
                </div>
              </div>
            ))}
            {!data?.score_trend?.length ? <p className="muted">Complete a mock interview to start trend tracking.</p> : null}
          </div>
        </section>
        <section className="card">
          <h3>Recent Activity</h3>
          <div className="stack">
            {(data?.recent_sessions || []).slice(0, 4).map((session) => (
              <div key={session.id}>
                <strong>{session.interview_type}</strong>
                <p className="muted">
                  {session.completed_count}/{session.question_count} answered · {session.difficulty}
                </p>
              </div>
            ))}
            {!data?.recent_sessions?.length ? <p className="muted">No recent sessions yet.</p> : null}
          </div>
        </section>
        <section className="card">
          <h3>AI Recommendations</h3>
          <div className="stack">
            <p className="muted">Upload your latest PDF resume before company-specific sessions.</p>
            <p className="muted">Run GitHub Analyzer after your portfolio README updates.</p>
            <p className="muted">Complete one mock interview to unlock targeted topic feedback.</p>
          </div>
        </section>
      </div>
    </AppShell>
  );
}
