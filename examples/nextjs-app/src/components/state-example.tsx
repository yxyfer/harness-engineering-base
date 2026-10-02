import Link from "next/link";
import { Button } from "./ui/button";

export type ExampleState =
  "loading" | "empty" | "error" | "no-access" | "success";
const content = {
  loading: [
    "Loading work items",
    "A static loading example, not a live request.",
  ],
  empty: [
    "No work items yet",
    "When a real workspace is empty, explain the next useful step.",
  ],
  error: [
    "We couldn’t load the work items",
    "Synthetic error example. No live service has failed.",
  ],
  "no-access": [
    "This workspace isn’t available",
    "Synthetic permission example, not an authorization control.",
  ],
  success: [
    "Preview updated",
    "Synthetic success example. Nothing has been persisted.",
  ],
} satisfies Record<ExampleState, readonly [string, string]>;

export function StateExample({ state }: { state: ExampleState }) {
  const [title, description] = content[state];
  return (
    <section
      className={`panel state state-${state}`}
      aria-busy={state === "loading"}
    >
      <p className="eyebrow">{state} · synthetic example</p>
      <h2>{title}</h2>
      <p className="muted">{description}</p>
      {state === "loading" ? (
        <div className="skeleton" aria-hidden="true" />
      ) : (
        <Button asChild variant="secondary">
          <Link href="/">Back to work items</Link>
        </Button>
      )}
    </section>
  );
}
