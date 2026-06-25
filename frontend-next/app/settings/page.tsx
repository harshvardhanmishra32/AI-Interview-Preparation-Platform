import { AppShell } from "@/components/AppShell";
import { PageHeader } from "@/components/PageHeader";

export default function SettingsPage() {
  return (
    <AppShell>
      <PageHeader eyebrow="Settings" title="Workspace Settings" description="Configure frontend deployment and account preferences." />
      <div className="cards-grid">
        <section className="card">
          <h3>Backend API URL</h3>
          <p className="muted">Set `NEXT_PUBLIC_API_URL` in Vercel to your Render backend URL.</p>
        </section>
        <section className="card">
          <h3>Security</h3>
          <p className="muted">Tokens are stored in browser local storage for this portfolio deployment. Use secure httpOnly cookies for a production SaaS rewrite.</p>
        </section>
        <section className="card">
          <h3>Theme</h3>
          <p className="muted">The Vercel frontend uses a professional light enterprise theme.</p>
        </section>
      </div>
    </AppShell>
  );
}
