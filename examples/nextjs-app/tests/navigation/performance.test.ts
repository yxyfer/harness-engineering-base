import { readdirSync, readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { gzipSync } from "node:zlib";
import { z } from "zod";
import { test, expect } from "./fixtures";
import { conditions } from "./ui-quality";

function clientBytes(directory: string): number {
  return readdirSync(directory, { withFileTypes: true }).reduce((sum, item) => {
    const path = join(directory, item.name);
    return (
      sum +
      (item.isDirectory()
        ? clientBytes(path)
        : item.name.endsWith(".js")
          ? gzipSync(readFileSync(path)).length
          : 0)
    );
  }, 0);
}

test("@ui performance: shipped client gzip and loopback navigation lab", async ({
  page,
  signIn,
}, info) => {
  await signIn();
  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  await cdp.send("Network.enable");
  await cdp.send("Network.setCacheDisabled", { cacheDisabled: true });
  await cdp.send("Network.emulateNetworkConditions", {
    offline: false,
    latency: 20,
    downloadThroughput: 1_250_000,
    uploadThroughput: 1_250_000,
  });
  const navigation: number[] = [];
  for (let sample = 0; sample < 5; sample++) {
    await page.goto("/work-items/WI-101", { waitUntil: "load" });
    await expect(page.getByLabel("Title", { exact: true })).toBeVisible();
    navigation.push(
      await page.evaluate(() => {
        const entry = performance.getEntriesByType("navigation")[0];
        if (!(entry instanceof PerformanceNavigationTiming))
          throw new Error("Missing native navigation timing");
        return entry.domContentLoadedEventEnd;
      }),
    );
  }
  const gzipBytes = clientBytes(".next/static/chunks");
  const measured = {
    label: "lab-only; not field Core Web Vitals or a route first-load budget",
    conditions: conditions(page),
    cpuSlowdown: 4,
    latencyMs: 20,
    megabitsPerSecond: 10,
    cache: "disabled; warm local server; five new document navigations",
    gzipBytes,
    navigationMs: navigation,
  };
  mkdirSync(".harness/reports/performance", { recursive: true });
  writeFileSync(
    ".harness/reports/performance/measurements.json",
    JSON.stringify(measured, null, 2),
  );
  await info.attach("lab measurements", {
    body: JSON.stringify(measured),
    contentType: "application/json",
  });
  const budget = z
    .object({
      clientGzipBytes: z.number().positive(),
      navigationMs: z.number().positive(),
    })
    .strict()
    .parse(JSON.parse(readFileSync("tests/performance-budgets.json", "utf8")));
  expect(gzipBytes, "all shipped client JS gzip budget").toBeLessThanOrEqual(
    budget.clientGzipBytes,
  );
  expect(Math.max(...navigation), "lab navigation budget").toBeLessThanOrEqual(
    budget.navigationMs,
  );
});
