import { expect, it } from "vitest";
import { canAccess } from "@/domain/access";

it("requires tenant and owner for reads and an editor role for writes", () => {
  const principal = { id: "alex", tenant: "north", role: "editor" as const };
  const item = { ownerId: "alex", tenant: "north" };
  expect(canAccess(principal, item, "read")).toBe(true);
  expect(canAccess(principal, item, "write")).toBe(true);
  expect(canAccess({ ...principal, role: "viewer" }, item, "read")).toBe(true);
  expect(canAccess({ ...principal, role: "viewer" }, item, "write")).toBe(
    false,
  );
  expect(canAccess(principal, { ...item, ownerId: "sam" }, "read")).toBe(false);
  expect(canAccess(principal, { ...item, tenant: "south" }, "write")).toBe(
    false,
  );
});
