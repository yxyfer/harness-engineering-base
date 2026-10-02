import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    name: "server",
    sequence: { groupOrder: 0 },
    environment: "node",
    include: ["tests/server/*.test.ts"],
    maxWorkers: 1,
    fileParallelism: false,
    testTimeout: 30_000,
    hookTimeout: 30_000,
    reporters: ["default", "junit"],
    outputFile: { junit: ".harness/reports/server.xml" },
  },
});
