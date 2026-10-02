import { spawn } from "node:child_process";
import {
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { basename, join, resolve } from "node:path";
import { setTimeout as pause } from "node:timers/promises";
import { z } from "zod";

// Fixture lifecycle belongs to the native runner, never production routes.
mkdirSync(".harness/tmp", { recursive: true });
const directory = mkdtempSync(resolve(".harness/tmp/workroom-browser-"));
const runner = spawn(
  process.execPath,
  ["node_modules/@playwright/test/cli.js", "test", ...process.argv.slice(2)],
  {
    stdio: "inherit",
    detached: true,
    env: { ...process.env, WORKROOM_DB_DIR: directory },
  },
);
let interrupted = false;
function signalRunner(signal: NodeJS.Signals) {
  if (!runner.pid) return;
  try {
    process.kill(-runner.pid, signal);
  } catch (error) {
    if (!(error instanceof Error && "code" in error && error.code === "ESRCH"))
      throw error;
  }
}
const deadline = setTimeout(() => {
  interrupted = true;
  signalRunner("SIGTERM");
  setTimeout(() => signalRunner("SIGKILL"), 5_000).unref();
}, 180_000);
deadline.unref();
for (const signal of ["SIGINT", "SIGTERM"] as const)
  process.on(signal, () => {
    interrupted = true;
    signalRunner(signal);
    setTimeout(() => signalRunner("SIGKILL"), 5_000).unref();
  });
runner.on("error", () => {
  rmSync(directory, { recursive: true, force: true });
  process.exitCode = 1;
});
async function stopServer() {
  const marker = join(directory, "server-process.json");
  if (!existsSync(marker)) return;
  const owned = z
    .object({
      parent: z.number().int().positive(),
      child: z.number().int().positive(),
    })
    .parse(JSON.parse(readFileSync(marker, "utf8")));
  function signal(pid: number, value: NodeJS.Signals) {
    try {
      process.kill(pid, value);
    } catch (error) {
      if (!(
        error instanceof Error &&
        "code" in error &&
        error.code === "ESRCH"
      ))
        throw error;
    }
  }
  function alive(pid: number) {
    try {
      process.kill(pid, 0);
      return true;
    } catch (error) {
      if (error instanceof Error && "code" in error && error.code === "ESRCH")
        return false;
      throw error;
    }
  }
  signal(owned.parent, "SIGTERM");
  signal(owned.child, "SIGTERM");
  const until = Date.now() + 3_000;
  while ((alive(owned.child) || alive(owned.parent)) && Date.now() < until)
    await pause(25); // Bounded process-exit observation, not a UI timing sleep.
  if (alive(owned.child)) signal(owned.child, "SIGKILL");
  if (alive(owned.parent)) signal(owned.parent, "SIGKILL");
}
runner.on("exit", (code) => {
  void finish(code);
});
async function finish(code: number | null) {
  // Explicit ownership also covers SIGINT before Playwright installs teardown.
  await stopServer();
  signalRunner("SIGTERM");
  rmSync(directory, { recursive: true, force: true });
  clearTimeout(deadline);
  mkdirSync(".harness/reports", { recursive: true });
  writeFileSync(
    ".harness/reports/journey-lifecycle.json",
    JSON.stringify({
      directory: basename(directory),
      cleaned: true,
      interrupted,
      exit: code,
    }) + "\n",
  );
  process.exitCode = interrupted ? 1 : (code ?? 1);
}
