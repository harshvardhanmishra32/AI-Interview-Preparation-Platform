import { AppShell } from "@/components/AppShell";
import { PageHeader } from "@/components/PageHeader";

export default function FeedbackPage() {
  return (
    <AppShell>
      <PageHeader eyebrow="Interview Feedback" title="Feedback Workspace" description="Submit answers in Mock Interview to generate scoring, missing concepts, and ideal answer feedback." />
      <div className="card">
        <h3>How feedback works</h3>
        <p className="muted">Each submitted answer is evaluated by the backend and saved with score, feedback, missing concepts, suggestions, and an ideal answer.</p>
      </div>
    </AppShell>
  );
}
