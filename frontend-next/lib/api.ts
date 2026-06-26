export type ApiResult<T> = { ok: true; data: T } | { ok: false; error: string };

type ApiRequestOptions = RequestInit & {
  timeoutMs?: number;
};

export type UserProfile = {
  id: number;
  name: string;
  email: string;
  education?: string | null;
  target_role?: string | null;
  created_at: string;
};

export type TokenResponse = {
  access_token: string;
  refresh_token?: string | null;
  token_type: string;
  expires_in?: number | null;
  user?: UserProfile | null;
};

export type DashboardData = {
  total_interviews: number;
  average_score: number;
  strongest_topics: string[];
  weakest_topics: string[];
  recent_sessions: RecentSession[];
  score_trend: { date: string; average_score: number }[];
};

export type RecentSession = {
  id: number;
  company?: string | null;
  role: string;
  interview_type: string;
  difficulty: string;
  created_at: string;
  question_count: number;
  completed_count: number;
  average_score?: number | null;
};

export type AnalyticsData = {
  topic_performance: { topic: string; average_score: number; question_count: number }[];
  weekly_progress: { week: string; average_score: number; interview_count: number }[];
  skill_growth: Record<string, unknown>[];
};

export type ResumeAnalysis = {
  id: number;
  user_id: number;
  skills?: string[] | null;
  projects?: string[] | null;
  certifications?: string[] | null;
  experience?: string[] | null;
  education_details?: string[] | null;
  summary?: string | null;
  strengths?: string[] | null;
  missing_skills?: string[] | null;
  suggestions?: string[] | null;
  uploaded_at: string;
};

export type InterviewSession = {
  id: number;
  company?: string | null;
  role: string;
  interview_type: string;
  difficulty: string;
  status: string;
  created_at: string;
  questions: QuestionDetail[];
};

export type QuestionDetail = {
  id: number;
  question_text: string;
  difficulty: string;
  topic: string;
  expected_concepts?: string[] | null;
  answer?: AnswerResponse | null;
};

export type AnswerResponse = {
  id: number;
  question_id: number;
  answer_text: string;
  score?: number | null;
  feedback?: string | null;
  missing_concepts?: string[] | null;
  suggestions?: string[] | null;
  ideal_answer?: string | null;
  evaluated_at?: string | null;
};

export type GitHubAnalysis = {
  username: string;
  repositories: { name: string; description?: string | null; language?: string | null; stars: number; forks: number }[];
  languages: Record<string, number>;
  total_repos: number;
  contribution_summary: string;
  project_questions: { project_name: string; question: string; expected_concepts: string[] }[];
  skill_assessment: string[];
  recommendations: string[];
};

export type CareerRoadmap = {
  skill_gaps: string[];
  learning_path: { skill: string; resource: string; duration: string; priority: string }[];
  recommended_certifications: string[];
  suggested_projects: { title: string; description: string; skills_practiced: string[] }[];
  timeline: string;
  career_roadmap: { phase: string; duration: string; goals: string[]; milestones: string[] }[];
};

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function parseError(response: Response, fallback: string): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: unknown };
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail) && body.detail.length > 0) {
      const first = body.detail[0] as { msg?: string };
      return first.msg || fallback;
    }
  } catch {
    return fallback;
  }
  return fallback;
}

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
  token?: string | null
): Promise<ApiResult<T>> {
  const { timeoutMs = 45000, signal, ...requestOptions } = options;
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs);

  if (signal) {
    if (signal.aborted) controller.abort();
    signal.addEventListener("abort", () => controller.abort(), { once: true });
  }

  try {
    const headers = new Headers(requestOptions.headers);
    if (!(requestOptions.body instanceof FormData) && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
    if (token) headers.set("Authorization", `Bearer ${token}`);

    const response = await fetch(`${API_URL}${path}`, {
      ...requestOptions,
      headers,
      cache: "no-store",
      signal: controller.signal
    });

    if (!response.ok) {
      return { ok: false, error: await parseError(response, "Request failed. Please try again.") };
    }

    return { ok: true, data: (await response.json()) as T };
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      return { ok: false, error: "The backend is taking too long to respond. Please try again in a moment." };
    }
    return { ok: false, error: "Cannot reach the backend. Check the Render API URL." };
  } finally {
    window.clearTimeout(timeout);
  }
}

export async function warmBackend(): Promise<boolean> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 8000);

  try {
    const response = await fetch(`${API_URL}/health`, {
      cache: "no-store",
      signal: controller.signal
    });
    return response.ok;
  } catch {
    return false;
  } finally {
    window.clearTimeout(timeout);
  }
}

export async function uploadResume(file: File, token: string): Promise<ApiResult<ResumeAnalysis>> {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest<ResumeAnalysis>("/api/resume/upload-resume", { method: "POST", body: formData }, token);
}
