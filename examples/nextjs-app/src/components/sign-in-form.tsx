"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "./ui/button";
import { Field } from "./ui/field";

export function SignInForm() {
  const router = useRouter();
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  async function submit(form: HTMLFormElement) {
    setBusy(true);
    setError(undefined);
    const data = new FormData(form);
    try {
      const result = await fetch("/api/session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: data.get("username"),
          password: data.get("password"),
        }),
      });
      if (!result.ok) {
        setError("Sign in failed. Check the local credentials.");
        return;
      }
      router.replace("/");
      router.refresh();
    } catch {
      setError("Sign in unavailable. Try again.");
    } finally {
      setBusy(false);
    }
  }
  return (
    <form
      className="panel editor"
      onSubmit={(event) => {
        event.preventDefault();
        void submit(event.currentTarget);
      }}
    >
      <Field
        id="username"
        name="username"
        label="Synthetic username"
        autoComplete="username"
        required
      />
      <Field
        id="password"
        name="password"
        label="Local password"
        type="password"
        autoComplete="current-password"
        required
      />
      {error && <p role="alert">{error}</p>}
      <Button disabled={busy}>Sign in</Button>
    </form>
  );
}
