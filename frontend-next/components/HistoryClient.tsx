"use client";

import { useEffect, useState } from "react";
import { apiRequest, InterviewSession } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

export function HistoryClient() {
  const { token } = useAuth();
  const [sessions, setSessions] = useState<InterviewSession[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    apiRequest<InterviewSession[]>("/api/interview/history", {}, token).then((result) => {
      if (result.ok) setSessions(result.data);
      else setError(result.error);
    });
  }, [token]);

  return (
    <AppShell>
      <PageHeader eyebrow="Interview History" title="Session History" description="Review previous mock interview sessions and completion status." />
      {error ? <div className="alert error">{error}</div> : null}
      <div className="stack">
        {sessions.map((session) => (
          <article className="card" key={session.id}>
            <div className="toolbar">
              <div>
                <h3>{session.interview_type} · {session.difficulty}</h3>
                <p className="muted">{session.company || "General"} · {new Date(session.created_at).toLocaleString()}</p>
              </div>
              <span className="badge">{session.questions.length} questions</span>
            </div>
          </article>
        ))}
        {!sessions.length ? <div className="card">No interview sessions yet.</div> : null}
      </div>
    </AppShell>
  );
}
