import "server-only";
import { z } from "zod";
import { canAccess, type Principal } from "../domain/access";
import { statuses } from "../domain/work-item";
import { openDatabase, transaction } from "./database.ts";

const rowSchema = z.object({
  id: z.string(),
  title: z.string(),
  summary: z.string(),
  status: z.enum(statuses),
  owner: z.string(),
  version: z.number(),
  tenant: z.string(),
  ownerId: z.string(),
});
const select = `SELECT w.id,w.title,w.summary,w.status,w.version,w.tenant,
  w.owner_id AS ownerId,u.name AS owner FROM work_items w
  JOIN users u ON u.id=w.owner_id`;

function dto(row: z.infer<typeof rowSchema>) {
  return {
    id: row.id,
    title: row.title,
    summary: row.summary,
    status: row.status,
    owner: row.owner,
    version: row.version,
  };
}

export function listWorkItems(principal: Principal) {
  const db = openDatabase();
  try {
    return db
      .prepare(`${select} WHERE w.tenant=? AND w.owner_id=? ORDER BY w.id`)
      .all(principal.tenant, principal.id)
      .map((row) => dto(rowSchema.parse(row)));
  } finally {
    db.close();
  }
}

export function findWorkItem(principal: Principal, id: string) {
  const db = openDatabase();
  try {
    const row = db.prepare(`${select} WHERE w.id=?`).get(id);
    if (!row) return;
    const resource = rowSchema.parse(row);
    return canAccess(principal, resource, "read") ? dto(resource) : undefined;
  } finally {
    db.close();
  }
}

export function updateWorkItem(
  principal: Principal,
  id: string,
  input: { title: string; status: (typeof statuses)[number]; version: number },
) {
  const db = openDatabase();
  try {
    return transaction(db, () => {
      const row = db.prepare(`${select} WHERE w.id=?`).get(id);
      if (!row) return { error: "not-found" as const };
      const resource = rowSchema.parse(row);
      if (!canAccess(principal, resource, "read"))
        return { error: "not-found" as const };
      if (!canAccess(principal, resource, "write"))
        return { error: "forbidden" as const };
      if (resource.version !== input.version)
        return { error: "conflict" as const };
      db.prepare(
        "UPDATE work_items SET title=?,status=?,version=version+1 WHERE id=? AND version=?",
      ).run(input.title, input.status, id, input.version);
      db.prepare(
        "INSERT INTO audit(item_id,actor_id,version) VALUES(?,?,?)",
      ).run(id, principal.id, input.version + 1);
      return {
        item: dto({ ...resource, ...input, version: input.version + 1 }),
      };
    });
  } finally {
    db.close();
  }
}
