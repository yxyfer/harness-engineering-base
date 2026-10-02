import { defineConfig } from "@playwright/test";

// Explicit setup installs here; verification never downloads a browser.
process.env.PLAYWRIGHT_BROWSERS_PATH ??= new URL(
  ".harness/tmp/browsers",
  import.meta.url,
).pathname;

export default defineConfig({
  testDir: "./tests/navigation",
  timeout: 30_000,
  retries: 0,
  workers: 1,
  updateSnapshots: "none",
  snapshotPathTemplate: "{testDir}/../visual-baselines/{arg}{ext}",
  outputDir: ".harness/reports/browser",
  reporter: [
    ["list"],
    [
      "junit",
      {
        outputFile:
          process.env.HARNESS_TEST_REPORT ?? ".harness/reports/navigation.xml",
      },
    ],
  ],
  use: {
    baseURL: "http://127.0.0.1:3100",
    browserName: "chromium",
    trace: "retain-on-failure",
    viewport: { width: 1440, height: 1000 },
    deviceScaleFactor: 1,
    locale: "en-GB",
    timezoneId: "UTC",
    reducedMotion: "reduce",
    colorScheme: "light",
  },
  webServer: {
    command: "node scripts/browser-server.ts",
    url: "http://127.0.0.1:3100",
    reuseExistingServer: false,
    timeout: 30_000,
    gracefulShutdown: { signal: "SIGTERM", timeout: 5_000 },
  },
});
