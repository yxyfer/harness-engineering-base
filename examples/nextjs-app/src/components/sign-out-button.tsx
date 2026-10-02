"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "./ui/button";

export function SignOutButton() {
  const router = useRouter();
  const [error, setError] = useState(false);
  async function signOut() {
    try {
      const response = await fetch("/api/session", { method: "DELETE" });
      if (!response.ok) {
        setError(true);
        return;
      }
      router.replace("/sign-in");
      router.refresh();
    } catch {
      setError(true);
    }
  }
  return (
    <>
      <Button
        variant="quiet"
        onClick={() => {
          void signOut();
        }}
      >
        Sign out
      </Button>
      {error && <span role="alert">Sign out failed. Try again.</span>}
    </>
  );
}
