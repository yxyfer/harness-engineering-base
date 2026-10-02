import { expect, test as base } from "@playwright/test";
import { z } from "zod";
import { openDatabase } from "../../src/server/database.ts";
import { localRuntime } from "../../src/server/local-runtime.ts";
import { seed } from "../../src/server/setup.ts";

export { expect };

export function stored(id = "WI-101") {
  const db = openDatabase();
  try {
    return z
      .object({
        title: z.string(),
        status: z.string(),
        version: z.number(),
        audits: z.number(),
      })
      .parse(
        db
          .prepare(
            `SELECT title,status,version,
      (SELECT count(*) FROM audit WHERE item_id=work_items.id) AS audits
      FROM work_items WHERE id=?`,
          )
          .get(id),
      );
  } finally {
    db.close();
  }
}

export function auditFault(enabled: boolean) {
  const db = openDatabase();
  try {
    db.exec(
      enabled
        ? `CREATE TRIGGER deny_audit BEFORE INSERT ON audit
      BEGIN SELECT RAISE(ABORT, 'synthetic audit dependency failure'); END`
        : "DROP TRIGGER IF EXISTS deny_audit",
    );
  } finally {
    db.close();
  }
}

type Fixtures = { signIn: (username?: string) => Promise<void>; guards: void };
export const test = base.extend<Fixtures>({
  signIn: async ({ context }, use) => {
    await seed(true);
    await use(async (username = "alex") => {
      const login = await context.request.post("/api/session", {
        headers: { Origin: "http://127.0.0.1:3100" },
        data: { username, password: localRuntime().syntheticPassword },
      });
      expect(login.status()).toBe(200);
    });
    auditFault(false);
  },
  guards: [
    async ({ page, context }, use, info) => {
      const errors: string[] = [];
      const expected = new Set<string>();
      page.on("pageerror", (error) => errors.push(error.message));
      page.on("console", (message) => {
        if (message.type() !== "error") return;
        const location = message.location().url;
        // Only this exact browser-generated resource error is expected for the
        // explicitly labelled negative route/status in this one test.
        const allowed = info.annotations.some(
          ({ type, description }) =>
            type === "expected-http-error" &&
            description ===
              `${new URL(location || "http://invalid").pathname}|${message.text()}`,
        );
        const key = `${location}|${message.text()}`;
        if (!allowed || expected.has(key)) errors.push(key);
        else expected.add(key);
      });
      await context.route("**/*", (route) => {
        const url = new URL(route.request().url());
        return url.origin === "http://127.0.0.1:3100"
          ? route.continue()
          : route.abort("blockedbyclient");
      });
      await use();
      expect(errors, "unexpected browser errors").toEqual([]);
    },
    { auto: true },
  ],
});
