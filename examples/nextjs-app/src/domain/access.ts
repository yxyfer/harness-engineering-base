export type Principal = {
  id: string;
  tenant: string;
  role: "editor" | "viewer";
};

export function canAccess(
  principal: Principal,
  resource: { ownerId: string; tenant: string },
  operation: "read" | "write",
): boolean {
  return (
    principal.id === resource.ownerId &&
    principal.tenant === resource.tenant &&
    (operation === "read" || principal.role === "editor")
  );
}
