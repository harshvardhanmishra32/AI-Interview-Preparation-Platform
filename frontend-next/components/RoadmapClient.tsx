"use client";

import { FormEvent, useState } from "react";
import { apiRequest, CareerRoadmap } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

export function RoadmapClient() {
  const { token, user } = useAuth();
  const [roadmap, setRoadmap] = useState<CareerRoadmap | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token) return;
    setLoading(true);
    setError("");
    const target_role = String(new FormData(event.currentTarget).get("target_role") || "");
    const result = await apiRequest<CareerRoadmap>("/api/career/generate-roadmap", { method: "POST", body: JSON.stringify({ target_role }) }, token);
    setLoading(false);
    if (result.ok) setRoadmap(result.data);
    else setError(result.error);
  }

  return (
    <AppShell>
      <PageHeader eyebrow="Career Roadmap" title="Personalized Career Roadmap" description="Generate learning milestones, certifications, and projects based on your preparation profile." />
      <form className="card form-grid" onSubmit={submit}>
        {error ? <div className="alert error" style={{ gridColumn: "1 / -1" }}>{error}</div> : null}
        <div className="field">
          <label htmlFor="target_role">Target Role</label>
          <input className="input" id="target_role" name="target_role" defaultValue={user?.target_role || "Software Engineer"} />
        </div>
        <button className="button" disabled={loading} type="submit">{loading ? "Generating..." : "Generate Roadmap"}</button>
      </form>
      {roadmap ? (
        <section className="stack" style={{ marginTop: 18 }}>
          <div className="card"><h3>Timeline</h3><p>{roadmap.timeline}</p></div>
          <div className="cards-grid">
            {roadmap.career_roadmap.map((phase) => (
              <article className="card" key={phase.phase}>
                <h3>{phase.phase}</h3>
                <p className="muted">{phase.duration}</p>
                {phase.goals.map((goal) => <p key={goal}>{goal}</p>)}
              </article>
            ))}
          </div>
          <div className="cards-grid">
            <article className="card"><h3>Skill Gaps</h3><div className="badge-list">{roadmap.skill_gaps.map((gap) => <span className="badge" key={gap}>{gap}</span>)}</div></article>
            <article className="card"><h3>Certifications</h3>{roadmap.recommended_certifications.map((cert) => <p key={cert}>{cert}</p>)}</article>
            <article className="card"><h3>Suggested Projects</h3>{roadmap.suggested_projects.map((project) => <p key={project.title}><strong>{project.title}</strong> {project.description}</p>)}</article>
          </div>
        </section>
      ) : null}
    </AppShell>
  );
}
