import { DatabaseSync } from "node:sqlite";
import { chmodSync } from "node:fs";
import { join } from "node:path";
import { localRuntime } from "./local-runtime.ts";

export function openDatabase() {
  const { directory } = localRuntime();
  const filename = join(directory, "data.sqlite");
  const db = new DatabaseSync(filename);
  chmodSync(filename, 0o600);
  db.exec("PRAGMA foreign_keys=ON; PRAGMA busy_timeout=2000;");
  return db;
}

export function transaction<T>(db: DatabaseSync, operation: () => T): T {
  db.exec("BEGIN IMMEDIATE");
  try {
    const result = operation();
    db.exec("COMMIT");
    return result;
  } catch (error) {
    db.exec("ROLLBACK");
    throw error;
  }
}

export function migrate() {
  const db = openDatabase();
  try {
    transaction(db, () => {
      db.exec(`
        CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY);
        CREATE TABLE IF NOT EXISTS users(
          id TEXT PRIMARY KEY, tenant TEXT NOT NULL, role TEXT NOT NULL
            CHECK(role IN ('editor','viewer')), name TEXT NOT NULL,
          password_hash TEXT NOT NULL, failures INTEGER NOT NULL DEFAULT 0,
          locked_until INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS sessions(
          id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id),
          expires_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS work_items(
          id TEXT PRIMARY KEY, tenant TEXT NOT NULL,
          owner_id TEXT NOT NULL REFERENCES users(id), title TEXT NOT NULL,
          summary TEXT NOT NULL, status TEXT NOT NULL
            CHECK(status IN ('Planned','In progress','Ready for review')),
          version INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE IF NOT EXISTS audit(
          id INTEGER PRIMARY KEY, item_id TEXT NOT NULL REFERENCES work_items(id),
          actor_id TEXT NOT NULL REFERENCES users(id), version INTEGER NOT NULL);
        INSERT OR IGNORE INTO schema_version VALUES(1);
      `);
      const rows = db.prepare("SELECT version FROM schema_version").all();
      if (rows.length !== 1 || rows[0]?.version !== 1)
        throw new Error(
          "Unsupported schema; review migration before proceeding.",
        );
    });
  } finally {
    db.close();
  }
}
