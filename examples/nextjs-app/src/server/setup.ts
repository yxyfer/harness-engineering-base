import {
  mkdirSync,
  writeFileSync,
  existsSync,
  chmodSync,
  readdirSync,
} from "node:fs";
import { randomBytes } from "node:crypto";
import { join } from "node:path";
import { hash } from "@node-rs/argon2";
import { safeDirectory, localRuntime } from "./local-runtime.ts";
import { migrate, openDatabase, transaction } from "./database.ts";

export function initialize(
  directory: string,
  origin = "http://127.0.0.1:3100",
) {
  safeDirectory(directory);
  mkdirSync(directory, { recursive: true, mode: 0o700 });
  const marker = join(directory, "runtime.json");
  if (!existsSync(marker)) {
    if (readdirSync(directory).length)
      throw new Error("Refusing to adopt an unmarked nonempty directory.");
    writeFileSync(
      marker,
      JSON.stringify({
        kind: "workroom-disposable-v1",
        origin,
        sessionSecret: randomBytes(48).toString("base64url"),
        syntheticPassword: randomBytes(24).toString("base64url"),
      }),
      { mode: 0o600, flag: "wx" },
    );
  }
  chmodSync(directory, 0o700);
  localRuntime();
  migrate();
}

export async function seed(reset = false) {
  const { syntheticPassword } = localRuntime();
  const passwordHash = await hash(syntheticPassword);
  const db = openDatabase();
  try {
    transaction(db, () => {
      if (reset)
        db.exec(
          "DELETE FROM audit; DELETE FROM sessions; DELETE FROM work_items; DELETE FROM users;",
        );
      for (const [id, tenant, role, name] of [
        ["alex", "north", "editor", "Alex Morgan"],
        ["sam", "north", "editor", "Sam Taylor"],
        ["viewer", "north", "viewer", "Jordan Lee"],
        ["outsider", "south", "editor", "Casey Rivers"],
      ]) {
        db.prepare(
          "INSERT OR IGNORE INTO users(id,tenant,role,name,password_hash) VALUES(?,?,?,?,?)",
        ).run(id!, tenant!, role!, name!, passwordHash);
      }
      for (const [id, owner, title, status] of [
        ["WI-101", "alex", "Review the onboarding journey", "In progress"],
        ["WI-102", "sam", "Prepare the weekly review", "Ready for review"],
        ["WI-103", "viewer", "Simplify the handover checklist", "Planned"],
      ]) {
        db.prepare(
          "INSERT OR IGNORE INTO work_items(id,tenant,owner_id,title,summary,status) VALUES(?,'north',?,?,?,?)",
        ).run(
          id!,
          owner!,
          title!,
          "Owned synthetic work; no customer records.",
          status!,
        );
      }
    });
  } finally {
    db.close();
  }
}
