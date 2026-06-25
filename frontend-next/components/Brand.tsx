import Link from "next/link";

export function Brand() {
  return (
    <Link className="brand" href="/">
      <span className="brand-mark">AI</span>
      <span>
        PREPAI
        <span className="brand-subtitle">Interview readiness OS</span>
      </span>
    </Link>
  );
}
