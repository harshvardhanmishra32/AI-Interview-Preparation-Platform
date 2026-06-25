"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, type ReactNode } from "react";
import { useAuth } from "@/lib/auth";
import { Brand } from "./Brand";

const navGroups = [
  {
    title: "Main",
    items: [
      ["Dashboard", "/dashboard"],
      ["Resume Analyzer", "/resume-analyzer"],
      ["Mock Interview", "/mock-interview"],
      ["Interview Feedback", "/feedback"],
      ["Company Interview", "/company-interview"],
      ["Interview History", "/interview-history"]
    ]
  },
  {
    title: "Tools",
    items: [
      ["Analytics", "/analytics"],
      ["Career Roadmap", "/career-roadmap"],
      ["GitHub Analyzer", "/github-analyzer"]
    ]
  },
  {
    title: "Account",
    items: [
      ["Profile", "/profile"],
      ["Settings", "/settings"]
    ]
  }
];

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { loading, isAuthenticated, logout, user } = useAuth();

  useEffect(() => {
    if (!loading && !isAuthenticated) router.replace("/login");
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <main className="page public-shell">
        <div className="card">Loading workspace...</div>
      </main>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <Brand />
        <div className="card" style={{ marginTop: 18, background: "rgba(255,255,255,0.04)", borderColor: "rgba(255,255,255,0.08)" }}>
          <strong>{user?.name || "Candidate"}</strong>
          <div className="muted" style={{ marginTop: 4, fontSize: "0.82rem" }}>
            {user?.target_role || "Interview candidate"}
          </div>
        </div>
        {navGroups.map((group) => (
          <nav className="nav-section" key={group.title} aria-label={group.title}>
            <p className="nav-section-title">{group.title}</p>
            {group.items.map(([label, href]) => (
              <Link className={`nav-link ${pathname === href ? "active" : ""}`} href={href} key={href}>
                {label}
              </Link>
            ))}
          </nav>
        ))}
        <button
          className="button danger full"
          style={{ marginTop: 22 }}
          onClick={() => {
            logout();
            router.push("/");
          }}
        >
          Logout
        </button>
      </aside>
      <main className="main">
        <div className="main-inner">{children}</div>
      </main>
    </div>
  );
}
