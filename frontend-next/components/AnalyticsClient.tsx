"use client";

import { useEffect, useState } from "react";
import { AnalyticsData, apiRequest } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

export function AnalyticsClient() {
  const { token } = useAuth();
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    apiRequest<AnalyticsData>("/api/analytics/analytics", {}, token).then((result) => {
      if (result.ok) setData(result.data);
      else setError(result.error);
    });
  }, [token]);

  return (
    <AppShell>
      <PageHeader eyebrow="Analytics" title="Performance Analytics" description="Review topic performance, weekly growth, and skill momentum from completed interview sessions." />
      {error ? <div className="alert error">{error}</div> : null}
      <div className="cards-grid">
        <section className="card">
          <h3>Topic Performance</h3>
          <div className="stack">
            {(data?.topic_performance || []).map((topic) => (
              <div key={topic.topic}>
                <div className="toolbar" style={{ marginBottom: 6 }}>
                  <span>{topic.topic}</span>
                  <strong>{topic.average_score.toFixed(1)}</strong>
                </div>
                <div className="bar"><span style={{ width: `${topic.average_score * 10}%` }} /></div>
              </div>
            ))}
            {!data?.topic_performance?.length ? <p className="muted">No topic data yet.</p> : null}
          </div>
        </section>
        <section className="card">
          <h3>Weekly Progress</h3>
          <div className="stack">
            {(data?.weekly_progress || []).map((week) => (
              <div key={week.week}>
                <strong>{week.week}</strong>
                <p className="muted">{week.interview_count} interviews · {week.average_score.toFixed(1)} average</p>
              </div>
            ))}
            {!data?.weekly_progress?.length ? <p className="muted">Complete interviews to populate weekly progress.</p> : null}
          </div>
        </section>
        <section className="card">
          <h3>Skill Growth</h3>
          <p className="muted">{data?.skill_growth?.length ? `${data.skill_growth.length} growth records available.` : "Skill growth appears after multiple sessions."}</p>
        </section>
      </div>
    </AppShell>
  );
}
