"use client";

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { apiRequest, TokenResponse, UserProfile } from "./api";

type AuthContextValue = {
  token: string | null;
  refreshToken: string | null;
  user: UserProfile | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string, rememberMe: boolean) => Promise<{ ok: boolean; error?: string }>;
  register: (payload: RegisterPayload) => Promise<{ ok: boolean; error?: string }>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
};

type RegisterPayload = {
  name: string;
  email: string;
  password: string;
  education: string;
  target_role: string;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("prepai_token");
    const savedRefresh = localStorage.getItem("prepai_refresh_token");
    const savedUser = localStorage.getItem("prepai_user");
    setToken(savedToken);
    setRefreshToken(savedRefresh);
    setUser(savedUser ? (JSON.parse(savedUser) as UserProfile) : null);
    setLoading(false);
  }, []);

  function persist(nextToken: string, nextRefresh: string | null, nextUser: UserProfile) {
    setToken(nextToken);
    setRefreshToken(nextRefresh);
    setUser(nextUser);
    localStorage.setItem("prepai_token", nextToken);
    if (nextRefresh) localStorage.setItem("prepai_refresh_token", nextRefresh);
    localStorage.setItem("prepai_user", JSON.stringify(nextUser));
  }

  function logout() {
    setToken(null);
    setRefreshToken(null);
    setUser(null);
    localStorage.removeItem("prepai_token");
    localStorage.removeItem("prepai_refresh_token");
    localStorage.removeItem("prepai_user");
  }

  async function login(email: string, password: string, rememberMe: boolean) {
    const result = await apiRequest<TokenResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password, remember_me: rememberMe }),
      timeoutMs: 15000
    });

    if (!result.ok) return { ok: false, error: result.error };

    const profile = result.data.user;
    if (profile) {
      persist(result.data.access_token, result.data.refresh_token || null, profile);
      return { ok: true };
    }

    const profileResult = await apiRequest<UserProfile>("/api/auth/profile", {}, result.data.access_token);
    if (!profileResult.ok) return { ok: false, error: profileResult.error };
    persist(result.data.access_token, result.data.refresh_token || null, profileResult.data);
    return { ok: true };
  }

  async function register(payload: RegisterPayload) {
    const result = await apiRequest<UserProfile>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
      timeoutMs: 20000
    });
    if (!result.ok) return { ok: false, error: result.error };
    return { ok: true };
  }

  async function refreshProfile() {
    if (!token) return;
    const result = await apiRequest<UserProfile>("/api/auth/profile", {}, token);
    if (result.ok) {
      setUser(result.data);
      localStorage.setItem("prepai_user", JSON.stringify(result.data));
    }
  }

  const value = useMemo(
    () => ({
      token,
      refreshToken,
      user,
      loading,
      isAuthenticated: Boolean(token),
      login,
      register,
      logout,
      refreshProfile
    }),
    [token, refreshToken, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}
