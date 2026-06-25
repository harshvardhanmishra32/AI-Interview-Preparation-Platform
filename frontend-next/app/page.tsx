import Link from "next/link";
import { PublicNav } from "@/components/PublicNav";

const features = [
  ["Resume Analyzer", "Upload PDF resumes, extract skills, and receive recruiter-grade improvement suggestions."],
  ["Mock Interview", "Generate role, company, and difficulty-aware questions with answer scoring."],
  ["GitHub Analyzer", "Review public repositories, language distribution, and project interview questions."],
  ["Career Roadmap", "Turn profile gaps into milestones, learning resources, certifications, and projects."],
  ["Analytics", "Track topic performance, score trends, weekly progress, and skill momentum."],
  ["Company Mode", "Prepare for Google, Amazon, Microsoft, TCS, Infosys, Accenture, and more."]
];

export default function LandingPage() {
  return (
    <main className="page public-shell">
      <PublicNav />
      <section className="hero">
        <div>
          <div className="eyebrow">AI Interview Readiness OS</div>
          <h1>Turn interview prep into measurable hiring readiness.</h1>
          <p>
            A focused SaaS workspace for resume signal, mock interview scoring, portfolio review, career planning,
            and analytics. Built for serious candidates and recruiter-ready demos.
          </p>
          <div className="hero-actions">
            <Link className="button" href="/register">
              Create Free Account
            </Link>
            <Link className="button secondary" href="/login">
              Log In
            </Link>
          </div>
        </div>
        <div className="preview" aria-label="Product preview">
          <div className="toolbar">
            <div>
              <strong>Candidate readiness report</strong>
              <div className="muted">Production dashboard preview</div>
            </div>
            <span className="badge">AI powered</span>
          </div>
          <div className="metric-grid">
            <div className="card">
              <div className="metric-label">Sessions</div>
              <div className="metric-value">24</div>
            </div>
            <div className="card">
              <div className="metric-label">Growth</div>
              <div className="metric-value" style={{ color: "var(--success)" }}>
                +18%
              </div>
            </div>
            <div className="card">
              <div className="metric-label">Focus</div>
              <div style={{ marginTop: 12, fontWeight: 850 }}>System Design</div>
            </div>
            <div className="card">
              <div className="metric-label">Resume</div>
              <div className="metric-value">82</div>
            </div>
          </div>
        </div>
      </section>
      <section>
        <div className="page-title">
          <div className="eyebrow">Features</div>
          <h1>Everything serious candidates need</h1>
          <p>A complete preparation loop from raw profile to measurable interview improvement.</p>
        </div>
        <div className="cards-grid">
          {features.map(([title, body]) => (
            <article className="card" key={title}>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
