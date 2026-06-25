"use client";

import { FormEvent, useState } from "react";
import { apiRequest, AnswerResponse, InterviewSession } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

export function InterviewClient({ companyMode = false }: { companyMode?: boolean }) {
  const { token } = useAuth();
  const [session, setSession] = useState<InterviewSession | null>(null);
  const [activeQuestion, setActiveQuestion] = useState<number | null>(null);
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState<AnswerResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function generate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token) return;
    setError("");
    setEvaluation(null);
    setLoading(true);
    const form = new FormData(event.currentTarget);
    const result = await apiRequest<InterviewSession>(
      "/api/interview/generate-questions",
      {
        method: "POST",
        body: JSON.stringify({
          interview_type: form.get("interview_type"),
          difficulty: form.get("difficulty"),
          question_count: Number(form.get("question_count")),
          company: String(form.get("company") || "") || null
        })
      },
      token
    );
    setLoading(false);
    if (result.ok) {
      setSession(result.data);
      setActiveQuestion(result.data.questions[0]?.id || null);
    } else setError(result.error);
  }

  async function submitAnswer() {
    if (!token || !activeQuestion || !answer.trim()) return;
    setLoading(true);
    const result = await apiRequest<AnswerResponse>(
      "/api/interview/submit-answer",
      { method: "POST", body: JSON.stringify({ question_id: activeQuestion, answer_text: answer }) },
      token
    );
    setLoading(false);
    if (result.ok) setEvaluation(result.data);
    else setError(result.error);
  }

  const active = session?.questions.find((question) => question.id === activeQuestion);

  return (
    <AppShell>
      <PageHeader
        eyebrow={companyMode ? "Company Interview" : "Mock Interview"}
        title={companyMode ? "Company Interview Mode" : "AI Mock Interview"}
        description="Generate interview questions, submit answers, and receive AI scoring with improvement feedback."
      />
      <form className="card form-grid" onSubmit={generate}>
        {error ? <div className="alert error" style={{ gridColumn: "1 / -1" }}>{error}</div> : null}
        <div className="field">
          <label htmlFor="interview_type">Interview Type</label>
          <select className="select" id="interview_type" name="interview_type">
            <option value="technical">Technical</option>
            <option value="hr">HR</option>
            <option value="behavioral">Behavioral</option>
            <option value="project_based">Project Based</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="difficulty">Difficulty</label>
          <select className="select" id="difficulty" name="difficulty">
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="question_count">Questions</label>
          <select className="select" id="question_count" name="question_count">
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="company">Company</label>
          <input className="input" id="company" name="company" placeholder={companyMode ? "Google, Amazon, Microsoft..." : "Optional"} />
        </div>
        <button className="button" disabled={loading} type="submit">
          {loading ? "Generating..." : "Generate Questions"}
        </button>
      </form>
      {session ? (
        <section className="cards-grid">
          <article className="card">
            <h3>Questions</h3>
            <div className="stack">
              {session.questions.map((question, index) => (
                <button className={`button ${activeQuestion === question.id ? "" : "secondary"}`} key={question.id} onClick={() => setActiveQuestion(question.id)}>
                  {index + 1}. {question.topic}
                </button>
              ))}
            </div>
          </article>
          <article className="card" style={{ gridColumn: "span 2" }}>
            <h3>{active?.question_text || "Select a question"}</h3>
            <p className="muted">{active?.expected_concepts?.join(", ")}</p>
            <textarea className="textarea" value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Write your answer here..." />
            <button className="button" disabled={loading || !activeQuestion} onClick={submitAnswer} style={{ marginTop: 12 }}>
              {loading ? "Evaluating..." : "Submit Answer"}
            </button>
            {evaluation ? (
              <div className="card" style={{ marginTop: 14 }}>
                <div className="metric-label">Score</div>
                <div className="metric-value">{evaluation.score?.toFixed(1)}/10</div>
                <p>{evaluation.feedback}</p>
                <strong>Ideal answer</strong>
                <p className="muted">{evaluation.ideal_answer}</p>
              </div>
            ) : null}
          </article>
        </section>
      ) : null}
    </AppShell>
  );
}
