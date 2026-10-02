import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { createConnection } from "node:net";
import { join } from "node:path";
import { z } from "zod";

const schema = z.object({
  directory: z.string().regex(/^workroom-browser-/),
  cleaned: z.literal(true),
  interrupted: z.boolean(),
  exit: z.number().nullable(),
});
async function check(interrupted: boolean) {
  const record = schema.parse(
    JSON.parse(readFileSync(".harness/reports/journey-lifecycle.json", "utf8")),
  );
  assert.equal(record.interrupted, interrupted);
  assert(!existsSync(join(".harness/tmp", record.directory)));
  await new Promise<void>((resolve, reject) => {
    const socket = createConnection({ host: "127.0.0.1", port: 3100 });
    socket.setTimeout(2_000, () => {
      socket.destroy();
      reject(new Error("cleanup probe timed out"));
    });
    socket.on("connect", () => {
      socket.destroy();
      reject(new Error("owned server still running"));
    });
    socket.on("error", (error) => {
      if ("code" in error && error.code === "ECONNREFUSED") resolve();
      else reject(error);
    });
  });
  return record;
}

const success = await check(false);
const runner = spawn(
  process.execPath,
  ["scripts/journeys.ts", "--grep", "@smoke"],
  { stdio: ["ignore", "pipe", "pipe"] },
);
let sent = false;
let output = "";
runner.stdout.on("data", (chunk: Buffer) => {
  output = (output + chunk.toString()).slice(-4_096);
  // Runner-accounted collection is an observable barrier, not an arbitrary
  // sleep. Interrupt before the worker begins its actual UI journey.
  if (!sent && output.includes("Running 1 test")) {
    sent = true;
    runner.kill("SIGINT");
  }
});
runner.stderr.on("data", () => {
  /* Drain bounded native diagnostics. */
});
const deadline = setTimeout(() => runner.kill("SIGTERM"), 30_000);
try {
  const code = await new Promise<number | null>((resolve, reject) => {
    runner.on("error", reject);
    runner.on("exit", resolve);
  });
  assert(sent, "native collection barrier was not reached");
  assert.equal(code, 1, "interrupted run must not pass");
  const interrupted = await check(true);
  writeFileSync(
    ".harness/reports/journey-cleanup.json",
    JSON.stringify({ success, interrupted, portRefused: true }, null, 2) + "\n",
  );
  console.log(
    "Success and SIGINT remove owned storage and stop the production server.",
  );
} finally {
  clearTimeout(deadline);
  runner.kill("SIGTERM");
}
