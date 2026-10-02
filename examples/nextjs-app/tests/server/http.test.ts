import { afterAll, beforeAll, beforeEach, expect, it } from "vitest";
import { spawn, type ChildProcess } from "node:child_process";
import { once } from "node:events";
import { createServer } from "node:net";
import {
  mkdtempSync,
  mkdirSync,
  writeFileSync,
  rmSync,
  symlinkSync,
} from "node:fs";
import { join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { initialize, seed } from "../../src/server/setup.ts";
import { openDatabase, migrate } from "../../src/server/database.ts";
import { localRuntime, safeDirectory } from "../../src/server/local-runtime.ts";
import { sealData } from "iron-session";

let directory: string;
let origin: string;
let child: ChildProcess | undefined;
let logs = "";
let password: string;
let secret: string;
const previousDirectory = process.env.WORKROOM_DB_DIR;

async function start() {
  child = spawn(
    process.execPath,
    [
      "node_modules/next/dist/bin/next",
      "start",
      "--hostname",
      "127.0.0.1",
      "--port",
      new URL(origin).port,
    ],
    {
      env: {
        ...process.env,
        WORKROOM_DB_DIR: directory,
        NEXT_TELEMETRY_DISABLED: "1",
      },
      stdio: ["ignore", "pipe", "pipe"],
    },
  );
  for (const stream of [child.stdout, child.stderr])
    stream?.on("data", (data: Buffer) => {
      logs = (logs + data.toString()).slice(-64_000);
    });
  const deadline = Date.now() + 15_000;
  while (Date.now() < deadline) {
    if (child.exitCode !== null)
      throw new Error("Production server failed to start.");
    try {
      if ((await fetch(`${origin}/sign-in`)).ok) return;
    } catch {
      /* readiness polling only */
    }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("Production server readiness deadline exceeded.");
}

async function stop() {
  if (!child || child.exitCode !== null) return;
  const exited = once(child, "exit");
  child.kill("SIGTERM");
  const timer = setTimeout(() => child?.kill("SIGKILL"), 3000);
  try {
    await exited;
  } finally {
    clearTimeout(timer);
  }
}

beforeAll(async () => {
  const listener = createServer();
  listener.listen(0, "127.0.0.1");
  await once(listener, "listening");
  const address = listener.address();
  if (!address || typeof address === "string")
    throw new Error("No disposable port.");
  origin = `http://127.0.0.1:${address.port}`;
  await new Promise<void>((resolve) => listener.close(() => resolve()));
  directory = mkdtempSync(join(tmpdir(), "workroom-http-"));
  process.env.WORKROOM_DB_DIR = directory;
  initialize(directory, origin);
  await seed();
  ({ syntheticPassword: password, sessionSecret: secret } = localRuntime());
  await start();
});
beforeEach(async () => {
  await seed(true);
});
afterAll(async () => {
  await stop();
  mkdirSync(".harness/reports", { recursive: true });
  writeFileSync(
    ".harness/reports/server.log",
    logs.replaceAll(password, "[REDACTED]").replaceAll(secret, "[REDACTED]"),
  );
  if (directory) rmSync(directory, { recursive: true, force: true });
  if (previousDirectory === undefined) delete process.env.WORKROOM_DB_DIR;
  else process.env.WORKROOM_DB_DIR = previousDirectory;
});

async function request(
  path: string,
  cookie = "",
  method = "GET",
  body?: unknown,
  extra: Record<string, string> = {},
) {
  return fetch(`${origin}${path}`, {
    method,
    headers: {
      Cookie: cookie,
      Origin: origin,
      "Content-Type": "application/json",
      ...extra,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
    redirect: "manual",
  });
}
async function signIn(username = "alex") {
  const response = await request("/api/session", "", "POST", {
    username,
    password,
  });
  expect(response.status).toBe(200);
  const cookie = response.headers.get("set-cookie");
  expect(cookie).toContain("HttpOnly");
  expect(cookie).toContain("SameSite=Strict");
  return cookie!.split(";")[0]!;
}
const change = {
  title: "Committed synthetic title",
  status: "Planned",
  version: 1,
};

it("anonymous direct reads and writes require real sign-in", async () => {
  expect((await request("/api/work-items")).status).toBe(401);
  expect(
    (await request("/api/work-items/WI-101", "", "PATCH", change)).status,
  ).toBe(401);
  expect((await request("/work-items/WI-101")).headers.get("location")).toBe(
    "/sign-in",
  );
});

it("real sessions allow owned reads, minimal DTOs and committed writes", async () => {
  const cookie = await signIn();
  const read = await request("/api/work-items/WI-101", cookie);
  expect(read.headers.get("cache-control")).toBe("private, no-store");
  expect(read.headers.get("vary")).toContain("Cookie");
  const body: unknown = await read.json();
  expect(body).toEqual({
    item: {
      id: "WI-101",
      title: "Review the onboarding journey",
      summary: "Owned synthetic work; no customer records.",
      owner: "Alex Morgan",
      status: "In progress",
      version: 1,
    },
  });
  expect(
    (await request("/api/work-items/WI-101", cookie, "PATCH", change)).status,
  ).toBe(200);
  expect(
    await (await request("/api/work-items/WI-101", cookie)).json(),
  ).toMatchObject({ item: { title: change.title, version: 2 } });
  const db = openDatabase();
  try {
    expect(db.prepare("SELECT version FROM audit").get()?.version).toBe(2);
  } finally {
    db.close();
  }
});

it("viewer reads owned work but role denies mutation", async () => {
  const cookie = await signIn("viewer");
  expect((await request("/api/work-items/WI-103", cookie)).status).toBe(200);
  expect(
    (await request("/api/work-items/WI-103", cookie, "PATCH", change)).status,
  ).toBe(403);
});

it("wrong owners cannot read or mutate a same-tenant item", async () => {
  const cookie = await signIn("sam");
  expect((await request("/api/work-items/WI-101", cookie)).status).toBe(404);
  expect(
    (await request("/api/work-items/WI-101", cookie, "PATCH", change)).status,
  ).toBe(404);
});

it("tenant scope still denies when the stored owner id matches", async () => {
  const cookie = await signIn("outsider");
  const db = openDatabase();
  try {
    db.prepare(
      "UPDATE work_items SET owner_id='outsider' WHERE id='WI-101'",
    ).run();
  } finally {
    db.close();
  }
  expect((await request("/api/work-items/WI-101", cookie)).status).toBe(404);
  expect(
    (await request("/api/work-items/WI-101", cookie, "PATCH", change)).status,
  ).toBe(404);
  expect(await (await request("/api/work-items", cookie)).json()).toEqual({
    items: [],
  });
});

it("strict invalid and malicious inputs never write", async () => {
  const cookie = await signIn();
  for (const invalid of [
    { ...change, title: "  " },
    { ...change, status: "admin" },
    { ...change, version: -1 },
    { ...change, tenant: "south" },
    { ...change, title: "bad\u0000title" },
    { ...change, title: "x".repeat(5000) },
  ]) {
    expect(
      (await request("/api/work-items/WI-101", cookie, "PATCH", invalid))
        .status,
    ).toBe(400);
  }
  const badJson = await fetch(`${origin}/api/work-items/WI-101`, {
    method: "PATCH",
    headers: {
      Cookie: cookie,
      Origin: origin,
      "Content-Type": "application/json",
    },
    body: "{broken",
  });
  expect(badJson.status).toBe(400);
  expect(
    (
      await request("/api/work-items/WI-101", cookie, "PATCH", change, {
        "Content-Type": "text/plain",
      })
    ).status,
  ).toBe(400);
  expect(
    (await request("/api/work-items/WI-101%27OR%201=1", cookie)).status,
  ).toBe(404);
  const db = openDatabase();
  try {
    expect(
      db.prepare("SELECT version FROM work_items WHERE id='WI-101'").get()
        ?.version,
    ).toBe(1);
    expect(db.prepare("SELECT COUNT(*) AS count FROM audit").get()?.count).toBe(
      0,
    );
  } finally {
    db.close();
  }
});

it("unsafe/missing/null origins, cross-site and forged Host are refused", async () => {
  const cookie = await signIn();
  const attempts: Record<string, string>[] = [
    { Origin: "https://attacker.invalid" },
    { Origin: "" },
    { Origin: "null" },
    { "Sec-Fetch-Site": "cross-site" },
    { Host: "attacker.invalid" },
  ];
  for (const headers of attempts) {
    expect(
      (
        await request(
          "/api/work-items/WI-101",
          cookie,
          "PATCH",
          change,
          headers,
        )
      ).status,
    ).toBe(403);
    expect(
      (
        await request(
          "/api/session",
          "",
          "POST",
          { username: "alex", password },
          headers,
        )
      ).status,
    ).toBe(403);
  }
});

it("tampered, expired and revoked sessions fail closed", async () => {
  const cookie = await signIn();
  expect(
    (await request("/api/work-items", cookie.replace("=", "=tampered"))).status,
  ).toBe(401);
  const expiredSeal = await sealData(
    { id: "no-session" },
    { password: secret, ttl: 1 },
  );
  await new Promise((resolve) => setTimeout(resolve, 2200));
  expect(
    (await request("/api/work-items", `workroom_session=${expiredSeal}`))
      .status,
  ).toBe(401);
  const db = openDatabase();
  try {
    db.prepare("UPDATE sessions SET expires_at=0").run();
  } finally {
    db.close();
  }
  expect(
    (await request("/api/work-items/WI-101", cookie, "PATCH", change)).status,
  ).toBe(401);
  const fresh = await signIn();
  expect((await request("/api/session", fresh, "DELETE")).status).toBe(200);
  expect((await request("/api/work-items", fresh)).status).toBe(401);
});

it("bad credentials and persistent login throttling never establish a session", async () => {
  for (let index = 0; index < 5; index++)
    expect(
      (
        await request("/api/session", "", "POST", {
          username: "alex",
          password: "not-the-password",
        })
      ).status,
    ).toBe(401);
  expect(
    (await request("/api/session", "", "POST", { username: "alex", password }))
      .status,
  ).toBe(401);
  expect(
    (
      await request("/api/session", "", "POST", {
        username: "unknown",
        password,
      })
    ).status,
  ).toBe(401);
  expect((await request("/api/work-items")).status).toBe(401);
});

it("audit storage failure rolls back the item and exposes only a safe error", async () => {
  const cookie = await signIn();
  const db = openDatabase();
  try {
    db.exec(
      "CREATE TRIGGER deny_audit BEFORE INSERT ON audit BEGIN SELECT RAISE(ABORT,'synthetic-private-storage-detail'); END;",
    );
  } finally {
    db.close();
  }
  try {
    const result = await request(
      "/api/work-items/WI-101",
      cookie,
      "PATCH",
      change,
    );
    expect(result.status).toBe(503);
    expect(await result.json()).toEqual({
      error: "Service unavailable. Try again.",
    });
    const inspection = openDatabase();
    try {
      expect(
        inspection
          .prepare("SELECT version FROM work_items WHERE id='WI-101'")
          .get()?.version,
      ).toBe(1);
      expect(
        inspection.prepare("SELECT COUNT(*) AS count FROM audit").get()?.count,
      ).toBe(0);
    } finally {
      inspection.close();
    }
    expect(logs).not.toContain("synthetic-private-storage-detail");
    expect(logs).not.toContain(password);
    expect(logs).not.toContain(secret);
  } finally {
    const cleanup = openDatabase();
    try {
      cleanup.exec("DROP TRIGGER deny_audit");
    } finally {
      cleanup.close();
    }
  }
});

it("fresh authorized reload and process restart retain committed storage and escape HTML", async () => {
  const cookie = await signIn();
  const title = "<script>alert(1)</script> '); DROP TABLE users;--";
  expect(
    (
      await request("/api/work-items/WI-101", cookie, "PATCH", {
        ...change,
        title,
      })
    ).status,
  ).toBe(200);
  expect(
    (await request("/api/work-items/WI-101", cookie, "PATCH", change)).status,
  ).toBe(409);
  const html = await (await request("/work-items/WI-101", cookie)).text();
  expect(html).toContain("&lt;script&gt;alert(1)&lt;/script&gt;");
  expect(html).not.toContain("<script>alert(1)</script>");
  await stop();
  await start();
  expect(
    await (await request("/api/work-items/WI-101", cookie)).json(),
  ).toMatchObject({ item: { title, version: 2 } });
  const other = await signIn("sam");
  expect((await request("/api/work-items/WI-101", other)).status).toBe(404);
  expect((await request("/work-items/WI-101", other)).status).not.toBe(503);
});

it("repeatable migrations/seeds preserve edits; guarded reset revokes sessions", async () => {
  const cookie = await signIn();
  await request("/api/work-items/WI-101", cookie, "PATCH", change);
  migrate();
  migrate();
  await seed();
  expect(
    await (await request("/api/work-items/WI-101", cookie)).json(),
  ).toMatchObject({ item: { title: change.title } });
  await seed(true);
  expect((await request("/api/work-items", cookie)).status).toBe(401);
});

it("unsafe production, traversal and symlink database targets are refused", () => {
  expect(() => safeDirectory("/production/database")).toThrow();
  expect(() => safeDirectory(".harness/tmp/workroom-local")).toThrow();
  expect(() => safeDirectory(`${directory}/../other`)).toThrow();
  const alias = resolve(directory, "../workroom-symlink-test");
  symlinkSync(directory, alias);
  try {
    expect(() => safeDirectory(alias)).toThrow(/Symlink/);
  } finally {
    rmSync(alias);
  }
  const original = process.env.DEPLOYMENT_ENV;
  process.env.DEPLOYMENT_ENV = "production";
  try {
    expect(() => localRuntime()).toThrow(/Production/);
  } finally {
    if (original === undefined) delete process.env.DEPLOYMENT_ENV;
    else process.env.DEPLOYMENT_ENV = original;
  }
});
