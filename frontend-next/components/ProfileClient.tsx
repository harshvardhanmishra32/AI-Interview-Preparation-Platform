"use client";

import { FormEvent, useState } from "react";
import { apiRequest, UserProfile } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { AppShell } from "./AppShell";
import { PageHeader } from "./PageHeader";

export function ProfileClient() {
  const { token, user, refreshProfile } = useAuth();
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token) return;
    setMessage("");
    setError("");
    const form = new FormData(event.currentTarget);
    const result = await apiRequest<UserProfile>(
      "/api/auth/profile",
      {
        method: "PUT",
        body: JSON.stringify({
          name: String(form.get("name")),
          email: String(form.get("email")),
          education: String(form.get("education")),
          target_role: String(form.get("target_role"))
        })
      },
      token
    );
    if (result.ok) {
      await refreshProfile();
      setMessage("Profile updated.");
    } else setError(result.error);
  }

  return (
    <AppShell>
      <PageHeader eyebrow="Profile" title="Candidate Profile" description="Keep your candidate identity and target role current for personalized preparation." />
      <form className="card form-grid" onSubmit={submit}>
        {message ? <div className="alert success" style={{ gridColumn: "1 / -1" }}>{message}</div> : null}
        {error ? <div className="alert error" style={{ gridColumn: "1 / -1" }}>{error}</div> : null}
        <div className="field"><label htmlFor="name">Name</label><input className="input" id="name" name="name" defaultValue={user?.name || ""} /></div>
        <div className="field"><label htmlFor="email">Email</label><input className="input" id="email" name="email" type="email" defaultValue={user?.email || ""} /></div>
        <div className="field"><label htmlFor="education">Education</label><input className="input" id="education" name="education" defaultValue={user?.education || ""} /></div>
        <div className="field"><label htmlFor="target_role">Target Role</label><input className="input" id="target_role" name="target_role" defaultValue={user?.target_role || ""} /></div>
        <button className="button" type="submit">Save Profile</button>
      </form>
    </AppShell>
  );
}
