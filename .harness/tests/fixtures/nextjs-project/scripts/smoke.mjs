import { spawn } from "node:child_process";
const child = spawn(process.execPath, ["scripts/server.mjs"], {
  env: { ...process.env, PORT: "0" },
  stdio: ["ignore", "pipe", "inherit"],
});

try {
  const url = await new Promise((resolve, reject) => {
    const timeout = setTimeout(
      () => reject(new Error("server did not become ready")),
      3000,
    );
    child.once("exit", (code) =>
      reject(new Error(`server exited before smoke check (${code})`)),
    );
    child.stdout.once("data", (chunk) => {
      clearTimeout(timeout);
      const match = chunk.toString().match(/http:\/\/127\.0\.0\.1:\d+/);
      match
        ? resolve(match[0])
        : reject(new Error("server did not report its URL"));
    });
  });
  const response = await fetch(url);
  const body = await response.text();
  if (!response.ok || !body.includes("Harness ready")) {
    throw new Error("golden-path content was not returned");
  }
  console.log("smoke: pass");
} finally {
  child.kill("SIGTERM");
}
