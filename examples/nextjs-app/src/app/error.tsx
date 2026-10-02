"use client";
import { Button } from "@/components/ui/button";
export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <section className="panel">
      <h1>Something went wrong</h1>
      <p>
        No internal error details are shown. This reference uses synthetic data.
      </p>
      <Button onClick={reset}>Try again</Button>
    </section>
  );
}
