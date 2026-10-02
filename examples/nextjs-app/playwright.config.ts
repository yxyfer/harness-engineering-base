import { defineConfig } from "@playwright/test";

// Explicit setup installs here; verification never downloads a browser.
process.env.PLAYWRIGHT_BROWSERS_PATH = new URL(
  ".harness/tmp/browsers",
  import.meta.url,
).pathname;

export default defineConfig({
  testDir: "./tests/navigation",
  timeout: 30_000,
  retries: 0,
  workers: 1,
  outputDir: ".harness/reports/browser",
  reporter: [
    ["list"],
    ["junit", { outputFile: ".harness/reports/navigation.xml" }],
  ],
  use: {
    baseURL: "http://127.0.0.1:3100",
    browserName: "chromium",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "npm run start",
    url: "http://127.0.0.1:3100",
    reuseExistingServer: false,
    timeout: 30_000,
  },
});
