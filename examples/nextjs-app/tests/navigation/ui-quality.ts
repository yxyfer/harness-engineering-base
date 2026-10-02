import AxeBuilder from "@axe-core/playwright";
import type { Page, TestInfo } from "@playwright/test";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync, readdirSync } from "node:fs";
import { release } from "node:os";
import { join } from "node:path";
import { expect } from "./fixtures";
import { z } from "zod";

const approvalSchema = z
  .object({
    status: z.literal("human-accepted"),
    reviewer: z.string().min(3),
    acceptedAt: z.iso.datetime(),
    conditions: z.record(z.string(), z.union([z.string(), z.number()])),
    images: z.record(z.string(), z.string().regex(/^[a-f0-9]{64}$/)),
  })
  .strict();

export function requireApproval(page: Page) {
  const path = "tests/visual-baselines/approval.json";
  let input: string;
  try {
    input = readFileSync(path, "utf8");
  } catch {
    throw new Error(
      "Human visual acceptance pending: missing approval.json; candidates are not baselines.",
    );
  }
  const approval = approvalSchema.parse(JSON.parse(input));
  expect(approval.conditions, "approved visual environment").toEqual(
    conditions(page),
  );
  return approval;
}

export const matrix = [
  { width: 390, theme: "paper" },
  { width: 390, theme: "ink" },
  { width: 1440, theme: "paper" },
  { width: 1440, theme: "ink" },
] as const;

export function sourceDigest() {
  const hash = createHash("sha256");
  function add(path: string) {
    for (const item of readdirSync(path, { withFileTypes: true }).sort((a, b) =>
      a.name.localeCompare(b.name),
    )) {
      const input = join(path, item.name);
      if (item.isDirectory()) add(input);
      else if (item.isFile()) hash.update(input).update(readFileSync(input));
      else throw new Error(`Unsafe visual source input: ${input}`);
    }
  }
  add("src");
  for (const path of [
    "package.json",
    "package-lock.json",
    "playwright.config.ts",
    "next.config.ts",
  ])
    hash.update(path).update(readFileSync(path));
  return hash.digest("hex");
}

export function conditions(page: Page) {
  return {
    browser: page.context().browser()?.version(),
    platform: process.platform,
    arch: process.arch,
    osRelease: release(),
    macOS: execFileSync("/usr/bin/sw_vers", ["-productVersion"], {
      encoding: "utf8",
    }).trim(),
    osBuild: execFileSync("/usr/bin/sw_vers", ["-buildVersion"], {
      encoding: "utf8",
    }).trim(),
    locale: "en-GB",
    timezone: "UTC",
    scale: 1,
    height: 1000,
    fonts: "local Arial/Helvetica",
    motion: "reduce; screenshot animations disabled; caret hidden",
    data: "synthetic seed v1",
  };
}

export async function theme(page: Page, value: string) {
  await expect(page.locator("main h1")).toBeVisible();
  if ((await page.locator("html").getAttribute("data-theme")) !== value)
    await page.getByRole("button", { name: "Switch theme" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", value);
}

export async function examine(page: Page, name: string, info: TestInfo) {
  // A fixed modal belongs to the visible viewport. Full-page stitching would
  // misleadingly paint its overlay over only one part of a taller document.
  const fullPage = !name.endsWith("-dialog");
  await expect(page.locator("main h1")).toBeVisible();
  // router.refresh streams metadata separately from the heading. Assert its
  // completed title instead of scanning a transient replacement document.
  await expect(page).toHaveTitle("Workroom · Synthetic reference");
  await page.evaluate(() => document.fonts.ready);
  if (info.title.includes("@visual-approved")) {
    const approval = requireApproval(page);
    const baseline = readFileSync(`tests/visual-baselines/${name}.png`);
    expect(createHash("sha256").update(baseline).digest("hex")).toBe(
      approval.images[name],
    );
    await expect(page).toHaveScreenshot(`${name}.png`, {
      fullPage,
      animations: "disabled",
      caret: "hide",
      threshold: 0.1,
      maxDiffPixels: 0,
    });
    return;
  }
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
    .analyze();
  await info.attach(`${name}-axe`, {
    body: JSON.stringify({
      engine: result.testEngine,
      violations: result.violations,
      incomplete: result.incomplete,
    }),
    contentType: "application/json",
  });
  expect(result.violations, `${name}: axe violations`).toEqual([]);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth,
    ),
    `${name}: horizontal overflow`,
  ).toBeLessThanOrEqual(0);
  const directory = ".harness/reports/ui-candidates";
  mkdirSync(directory, { recursive: true });
  const path = join(directory, `${name}.png`);
  await page.screenshot({
    path,
    fullPage,
    animations: "disabled",
    caret: "hide",
  });
  writeFileSync(
    join(directory, `${name}.json`),
    JSON.stringify(
      {
        status: "candidate-not-approved",
        capture: fullPage ? "full-page" : "viewport",
        sourceDigest: sourceDigest(),
        conditions: conditions(page),
        viewport: page.viewportSize(),
        sha256: createHash("sha256").update(readFileSync(path)).digest("hex"),
      },
      null,
      2,
    ),
  );
  await info.attach(name, { path, contentType: "image/png" });
  // Retained in native JUnit stdout as well as metadata, so the delegated
  // evidence binds actual candidate pixels without treating them as accepted.
  console.log(
    `candidate ${name} sha256=${createHash("sha256").update(readFileSync(path)).digest("hex")} source=${sourceDigest()}`,
  );
}
