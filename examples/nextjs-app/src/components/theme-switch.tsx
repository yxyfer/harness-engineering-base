"use client";

import { useState } from "react";
import { Button } from "./ui/button";

export function ThemeSwitch() {
  const [theme, setTheme] = useState("paper");
  return (
    <Button
      variant="secondary"
      aria-label="Switch theme"
      aria-pressed={theme === "ink"}
      onClick={() => {
        const next = theme === "paper" ? "ink" : "paper";
        setTheme(next);
        document.documentElement.dataset.theme = next;
      }}
    >
      Theme: {theme === "paper" ? "Paper" : "Ink"}
    </Button>
  );
}
