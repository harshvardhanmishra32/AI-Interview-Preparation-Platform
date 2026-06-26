"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { warmBackend } from "@/lib/api";
import { Brand } from "./Brand";

const roles = [
  "Software Engineer",
  "Data Scientist",
  "Machine Learning Engineer",
  "Frontend Developer",
  "Backend Developer",
  "Full Stack Developer",
  "DevOps Engineer",
  "Product Manager"
];

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const router = useRouter();
  const auth = useAuth();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendReady, setBackendReady] = useState(false);
  const [backendChecking, setBackendChecking] = useState(true);

  useEffect(() => {
    let active = true;

    warmBackend().then((ready) => {
      if (!active) return;
      setBackendReady(ready);
      setBackendChecking(false);
    });

    return () => {
      active = false;
    };
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const form = new FormData(event.currentTarget);
      if (mode === "login") {
        const result = await auth.login(String(form.get("email")), String(form.get("password")), form.get("remember") === "on");
        if (!result.ok) {
          setError(result.error || "Login failed.");
          return;
        }
        router.push("/dashboard");
        return;
      }

      const password = String(form.get("password"));
      const confirmPassword = String(form.get("confirmPassword"));
      if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }

      const result = await auth.register({
        name: String(form.get("name")),
        email: String(form.get("email")),
        password,
        education: String(form.get("education")),
        target_role: String(form.get("targetRole"))
      });
      if (!result.ok) {
        setError(result.error || "Registration failed.");
        return;
      }
      setSuccess("Account created. Please log in.");
      router.push("/login");
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  const isRegister = mode === "register";
  const submitLabel = loading
    ? isRegister
      ? "Creating account..."
      : "Signing in..."
    : isRegister
      ? "Create Free Account"
      : "Access Workspace";

  return (
    <main className="page public-shell">
      <div className="topnav">
        <Brand />
        <Link className="button secondary" href="/">
          Back to Home
        </Link>
      </div>
      <section style={{ maxWidth: 500, margin: "56px auto 0" }}>
        <div className="page-title">
          <div className="eyebrow">Account Access</div>
          <h1>{isRegister ? "Create Free Account" : "Welcome Back"}</h1>
          <p>{isRegister ? "Build your candidate profile and start preparing." : "Log in to continue your interview workspace."}</p>
        </div>
        <div className="toolbar">
          <Link className={`button ${!isRegister ? "" : "secondary"}`} href="/login">
            Log In
          </Link>
          <Link className={`button ${isRegister ? "" : "secondary"}`} href="/register">
            Create Account
          </Link>
        </div>
        <form className="card stack" onSubmit={handleSubmit}>
          {error ? <div className="alert error">{error}</div> : null}
          {success ? <div className="alert success">{success}</div> : null}
          {backendChecking ? (
            <div className="alert">Connecting securely to the backend...</div>
          ) : null}
          {!backendChecking && !backendReady ? (
            <div className="alert error">The backend is waking up. Submit again in a few seconds if the first attempt is slow.</div>
          ) : null}
          {isRegister ? (
            <>
              <div className="field">
                <label htmlFor="name">Full Name</label>
                <input className="input" id="name" name="name" required minLength={2} placeholder="John Doe" />
              </div>
              <div className="field">
                <label htmlFor="education">Education / University</label>
                <input className="input" id="education" name="education" placeholder="B.S. in Computer Science" />
              </div>
              <div className="field">
                <label htmlFor="targetRole">Target Role</label>
                <select className="select" id="targetRole" name="targetRole">
                  {roles.map((role) => (
                    <option key={role}>{role}</option>
                  ))}
                </select>
              </div>
            </>
          ) : null}
          <div className="field">
            <label htmlFor="email">Email Address</label>
            <input className="input" id="email" name="email" required type="email" placeholder="name@example.com" />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input className="input" id="password" name="password" required type="password" minLength={8} placeholder="At least 8 characters" />
          </div>
          {isRegister ? (
            <div className="field">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input className="input" id="confirmPassword" name="confirmPassword" required type="password" minLength={8} />
            </div>
          ) : (
            <label style={{ display: "flex", gap: 8, alignItems: "center", color: "var(--muted)" }}>
              <input name="remember" type="checkbox" defaultChecked />
              Remember me for 7 days
            </label>
          )}
          <button className="button full" disabled={loading} type="submit">
            {submitLabel}
          </button>
        </form>
      </section>
    </main>
  );
}
