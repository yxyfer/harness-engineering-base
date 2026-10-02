import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { join } from "node:path";
import { initialize, seed } from "../src/server/setup.ts";

// Only the explicitly invoked native browser suite uses this owned fixture.
if (!process.env.WORKROOM_DB_DIR)
  throw new Error("Run browser fixtures through scripts/journeys.ts");
initialize(process.env.WORKROOM_DB_DIR);
await seed(true);
const server = spawn(
  process.execPath,
  [
    "node_modules/next/dist/bin/next",
    "start",
    "--hostname",
    "127.0.0.1",
    "--port",
    "3100",
  ],
  { stdio: "inherit" },
);
writeFileSync(
  join(process.env.WORKROOM_DB_DIR, "server-process.json"),
  JSON.stringify({ parent: process.pid, child: server.pid }),
  { mode: 0o600 },
);
for (const signal of ["SIGINT", "SIGTERM"] as const)
  process.on(signal, () => {
    server.kill(signal);
    setTimeout(() => server.kill("SIGKILL"), 3_000).unref();
  });
server.on("exit", (code) => {
  process.exitCode = code ?? 1;
});
