export function label(value: unknown): string {
  if (typeof value !== "string" || !value.trim()) {
    throw new TypeError("A non-empty label is required");
  }
  return value.trim();
}
