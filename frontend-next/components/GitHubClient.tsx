"use client";

import { FormEvent, useState } from "react";
import { apiRequest, GitHubAnalysis } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

export function GitHubClient() {
  const { token } = useAuth();
  const [analysis, setAnalysis] = useState<GitHubAnalysis | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token) return;
    setError("");
    setLoading(true);
    const github_url = String(new FormData(event.currentTarget).get("github_url"));
    const result = await apiRequest<GitHubAnalysis>("/api/github/analyze-github", { method: "POST", body: JSON.stringify({ github_url }) }, token);
    setLoading(false);
    if (result.ok) setAnalysis(result.data);
    else setError(result.error);
  }

  return (
    <AppShell>
      <PageHeader eyebrow="GitHub Analyzer" title="Portfolio Analysis" description="Analyze public repositories and generate portfolio-specific interview questions." />
      <form className="card stack" onSubmit={submit}>
        {error ? <div className="alert error">{error}</div> : null}
        <div className="field">
          <label htmlFor="github_url">GitHub Profile URL</label>
          <input className="input" id="github_url" name="github_url" placeholder="https://github.com/username" />
        </div>
        <button className="button" disabled={loading} type="submit">{loading ? "Analyzing..." : "Analyze GitHub"}</button>
      </form>
      {analysis ? (
        <section className="stack" style={{ marginTop: 18 }}>
          <div className="metric-grid">
            <div className="card"><div className="metric-label">Username</div><div className="metric-value">{analysis.username}</div></div>
            <div className="card"><div className="metric-label">Repos</div><div className="metric-value">{analysis.total_repos}</div></div>
            <div className="card"><div className="metric-label">Languages</div><div className="metric-value">{Object.keys(analysis.languages).length}</div></div>
            <div className="card"><div className="metric-label">Questions</div><div className="metric-value">{analysis.project_questions.length}</div></div>
          </div>
          <div className="cards-grid">
            <article className="card"><h3>Contribution Summary</h3><p>{analysis.contribution_summary}</p></article>
            <article className="card"><h3>Skill Assessment</h3>{analysis.skill_assessment.map((item) => <p key={item}>{item}</p>)}</article>
            <article className="card"><h3>Recommendations</h3>{analysis.recommendations.map((item) => <p key={item}>{item}</p>)}</article>
          </div>
          <div className="cards-grid">
            {analysis.project_questions.slice(0, 6).map((question) => (
              <article className="card" key={`${question.project_name}-${question.question}`}>
                <h3>{question.project_name}</h3>
                <p>{question.question}</p>
                <div className="badge-list">{question.expected_concepts.map((concept) => <span className="badge" key={concept}>{concept}</span>)}</div>
              </article>
            ))}
          </div>
        </section>
      ) : null}
    </AppShell>
  );
}
