import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": new URL("./src", import.meta.url).pathname } },
  test: {
    projects: [
      "./vitest.server.config.ts",
      {
        extends: true,
        test: { name: "components", sequence: { groupOrder: 1 } },
      },
    ],
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    include: ["tests/*.test.ts", "tests/*.test.tsx"],
    maxWorkers: 2,
    outputFile: {
      junit:
        process.env.HARNESS_TEST_REPORT ?? ".harness/reports/components.xml",
    },
  },
});
