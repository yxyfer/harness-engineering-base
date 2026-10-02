import { describe, expect, it } from "vitest";
import { titleError } from "@/domain/work-item";

describe("work-item titles", () => {
  it("rejects empty and short input", () => {
    expect(titleError("   ")).toBeDefined();
    expect(titleError("ab")).toBeDefined();
  });
  it("accepts trimmed boundary lengths", () => {
    expect(titleError(" abc ")).toBeUndefined();
    expect(titleError("a".repeat(80))).toBeUndefined();
  });
  it("rejects an oversized title", () => {
    expect(titleError("a".repeat(81))).toContain("80");
  });
});
