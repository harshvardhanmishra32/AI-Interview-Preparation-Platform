import Link from "next/link";
import { Brand } from "./Brand";

export function PublicNav() {
  return (
    <header className="topnav">
      <Brand />
      <nav className="topnav-actions" aria-label="Public navigation">
        <Link className="button secondary" href="/login">
          Log In
        </Link>
        <Link className="button secondary" href="/register">
          Sign Up
        </Link>
        <Link className="button" href="/register">
          Create Free Account
        </Link>
      </nav>
    </header>
  );
}
