import { getIronSession } from "iron-session";
import { cookies, headers } from "next/headers";
import { randomUUID } from "node:crypto";
import { verify } from "@node-rs/argon2";
import { z } from "zod";
import { openDatabase } from "./database.ts";
import { localRuntime } from "./local-runtime.ts";
import type { Principal } from "../domain/access";

const principalSchema = z.strictObject({
  id: z.string(),
  tenant: z.string(),
  role: z.enum(["editor", "viewer"]),
});

export async function sessionCookie() {
  const config = localRuntime();
  return getIronSession<{ id: string }>(await cookies(), {
    password: config.sessionSecret,
    cookieName: "workroom_session",
    ttl: 3600,
    // Non-loopback HTTP/production deployment is refused. No production bypass.
    cookieOptions: {
      secure: false,
      httpOnly: true,
      sameSite: "strict",
      path: "/",
      maxAge: 3600,
    },
  });
}

export async function currentPrincipal(): Promise<Principal | undefined> {
  if ((await headers()).get("host") !== new URL(localRuntime().origin).host)
    return;
  const session = await sessionCookie();
  const parsed = z.string().uuid().safeParse(session.id);
  if (!parsed.success) return;
  const db = openDatabase();
  try {
    const row = db
      .prepare(
        `SELECT u.id,u.tenant,u.role FROM sessions s
      JOIN users u ON u.id=s.user_id WHERE s.id=? AND s.expires_at>?`,
      )
      .get(parsed.data, Date.now());
    return row ? principalSchema.parse(row) : undefined;
  } finally {
    db.close();
  }
}

export async function login(
  username: string,
  password: string,
): Promise<boolean> {
  const db = openDatabase();
  try {
    const row = db
      .prepare("SELECT password_hash,locked_until FROM users WHERE id=?")
      .get(username);
    const fallback = db
      .prepare("SELECT password_hash FROM users LIMIT 1")
      .get();
    const passwordHash = row?.password_hash ?? fallback?.password_hash;
    if (typeof passwordHash !== "string") return false;
    const matched = await verify(passwordHash, password);
    if (!row || !matched || Number(row.locked_until) > Date.now()) {
      if (row)
        db.prepare(
          `UPDATE users SET failures=failures+1,
        locked_until=CASE WHEN failures>=4 THEN ? ELSE locked_until END WHERE id=?`,
        ).run(Date.now() + 60_000, username);
      return false;
    }
    const session = await sessionCookie();
    if (session.id)
      db.prepare("DELETE FROM sessions WHERE id=?").run(session.id);
    session.id = randomUUID();
    db.prepare("INSERT INTO sessions VALUES(?,?,?)").run(
      session.id,
      username,
      Date.now() + 3600_000,
    );
    db.prepare("UPDATE users SET failures=0,locked_until=0 WHERE id=?").run(
      username,
    );
    await session.save();
    return true;
  } finally {
    db.close();
  }
}

export async function logout() {
  const session = await sessionCookie();
  const db = openDatabase();
  try {
    if (session.id)
      db.prepare("DELETE FROM sessions WHERE id=?").run(session.id);
    session.destroy();
  } finally {
    db.close();
  }
}
