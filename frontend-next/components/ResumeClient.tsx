"use client";

import { FormEvent, useState } from "react";
import { uploadResume, ResumeAnalysis } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

function list(value?: string[] | null) {
  return value && value.length ? value : [];
}

export function ResumeClient() {
  const { token } = useAuth();
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);
    const file = (new FormData(event.currentTarget).get("resume") as File | null) || null;
    if (!file || file.size === 0 || !token) {
      setLoading(false);
      setError("Select a PDF resume before processing.");
      return;
    }
    const result = await uploadResume(file, token);
    setLoading(false);
    if (result.ok) setAnalysis(result.data);
    else setError(result.error);
  }

  return (
    <AppShell>
      <PageHeader eyebrow="Resume Analyzer" title="Resume Analysis" description="Upload a PDF resume to extract skills, projects, gaps, and improvement suggestions." />
      <form className="card stack" onSubmit={handleSubmit}>
        {error ? <div className="alert error">{error}</div> : null}
        <div className="field">
          <label htmlFor="resume">PDF Resume</label>
          <input className="input" id="resume" name="resume" type="file" accept="application/pdf" />
        </div>
        <button className="button" disabled={loading} type="submit">
          {loading ? "Analyzing..." : "Process & Analyze Resume"}
        </button>
      </form>
      {analysis ? (
        <section className="stack" style={{ marginTop: 18 }}>
          <div className="metric-grid">
            <div className="card"><div className="metric-label">Skills</div><div className="metric-value">{list(analysis.skills).length}</div></div>
            <div className="card"><div className="metric-label">Projects</div><div className="metric-value">{list(analysis.projects).length}</div></div>
            <div className="card"><div className="metric-label">Gaps</div><div className="metric-value">{list(analysis.missing_skills).length}</div></div>
            <div className="card"><div className="metric-label">Suggestions</div><div className="metric-value">{list(analysis.suggestions).length}</div></div>
          </div>
          <div className="cards-grid">
            <article className="card">
              <h3>Professional Summary</h3>
              <p>{analysis.summary || "No summary returned."}</p>
            </article>
            <article className="card">
              <h3>Skills</h3>
              <div className="badge-list">{list(analysis.skills).map((skill) => <span className="badge" key={skill}>{skill}</span>)}</div>
            </article>
            <article className="card">
              <h3>Skill Gaps</h3>
              <div className="badge-list">{list(analysis.missing_skills).map((skill) => <span className="badge" key={skill}>{skill}</span>)}</div>
            </article>
          </div>
          <div className="cards-grid">
            <article className="card"><h3>Projects</h3>{list(analysis.projects).map((item) => <p key={item}>{item}</p>)}</article>
            <article className="card"><h3>Strengths</h3>{list(analysis.strengths).map((item) => <p key={item}>{item}</p>)}</article>
            <article className="card"><h3>Suggestions</h3>{list(analysis.suggestions).map((item) => <p key={item}>{item}</p>)}</article>
          </div>
        </section>
      ) : null}
    </AppShell>
  );
}
