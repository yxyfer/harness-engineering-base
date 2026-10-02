import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  cpSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { basename, join, resolve } from "node:path";

// Generated negative-control copies only. Synthetic comparator fixtures are
// never human acceptance and never copied back into maintained baseline files.
const source = resolve(".");
const owned = mkdtempSync(join(realpathSync(tmpdir()), "workroom-ui-mutants-"));
const reportRoot = resolve(".harness/reports/ui-regressions");
mkdirSync(reportRoot, { recursive: true });
const reports = mkdtempSync(join(reportRoot, "run-"));
const env: NodeJS.ProcessEnv = {
  ...process.env,
  PLAYWRIGHT_BROWSERS_PATH: resolve(".harness/tmp/browsers"),
};
function run(copy: string, name: string, argv: string[]) {
  const result = spawnSync(process.execPath, argv, {
    cwd: copy,
    env,
    timeout: 180_000,
    encoding: "utf8",
    maxBuffer: 4 * 1024 * 1024,
  });
  writeFileSync(
    join(reports, `${name}.log`),
    (result.stdout + result.stderr).slice(0, 65_536),
  );
  assert(!result.error && !result.signal, `${name}: infrastructure failed`);
  return result.status;
}
function change(copy: string, file: string, before: string, after: string) {
  const path = join(copy, file);
  const text = readFileSync(path, "utf8");
  assert.equal(text.split(before).length, 2, `${file}: unique mutation anchor`);
  writeFileSync(path, text.replace(before, after));
}
function duplicate(kind: string) {
  const copy = join(owned, kind);
  mkdirSync(copy);
  const excluded = ["node_modules", ".next", "tmp", "reports", ".git"];
  for (const name of readdirSync(source)) {
    if (excluded.includes(name)) continue;
    if (name === ".harness") {
      mkdirSync(join(copy, name));
      for (const input of readdirSync(join(source, name)))
        if (!excluded.includes(input))
          cpSync(join(source, name, input), join(copy, name, input), {
            recursive: true,
          });
    } else
      cpSync(join(source, name), join(copy, name), {
        recursive: true,
        filter: (path) => !excluded.includes(basename(path)),
      });
  }
  symlinkSync(join(source, "node_modules"), join(copy, "node_modules"), "dir");
  return copy;
}
try {
  for (const kind of [
    "label",
    "focus",
    "overflow",
    "appearance",
    "budget",
  ] as const) {
    const copy = duplicate(kind);
    let grep = "@ui states 390-paper";
    let expected = /axe violations/;
    if (kind === "label")
      change(
        copy,
        "src/components/ui/field.tsx",
        "<label htmlFor={id}>",
        "<label htmlFor={`${id}-missing`}>",
      );
    if (kind === "focus") {
      change(
        copy,
        "src/app/globals.css",
        "outline: 2px solid var(--ring);",
        "outline: none;",
      );
      grep = "@ui keyboard 390-paper";
      expected = /visible keyboard focus/;
    }
    if (kind === "overflow") {
      change(
        copy,
        "src/app/globals.css",
        "min-width: 0;",
        "min-width: 2000px;",
      );
      expected = /horizontal overflow/;
    }
    if (kind === "appearance") {
      // Healthy native comparator control first, using explicitly unapproved
      // pixels solely inside this disposable copy.
      cpSync(join(source, ".next"), join(copy, ".next"), { recursive: true });
      cpSync(
        join(source, ".harness/reports/ui-candidates/390-paper-list.png"),
        join(copy, "tests/visual-baselines/390-paper-list.png"),
      );
      writeFileSync(
        join(copy, "tests/navigation/visual-control.test.ts"),
        `
import { test, expect } from "./fixtures";
test("@visual-control synthetic comparator, not human acceptance", async ({page,signIn}) => {
  await signIn(); await page.setViewportSize({width:390,height:1000});
  await page.goto("/"); await expect(page).toHaveTitle("Workroom · Synthetic reference");
  await expect(page.locator("main h1")).toBeVisible();
  await page.evaluate(() => document.fonts.ready);
  await expect(page).toHaveScreenshot("390-paper-list.png", {
    fullPage:true, animations:"disabled", caret:"hide", threshold:0.1,maxDiffPixels:0,
  });
});
`,
      );
      env.HARNESS_TEST_REPORT = join(reports, "appearance-healthy.xml");
      assert.equal(
        run(copy, "appearance-healthy", [
          "scripts/journeys.ts",
          "--grep",
          "@visual-control",
        ]),
        0,
        "healthy comparator must match pinned candidate pixels",
      );
      change(
        copy,
        "src/app/globals.css",
        "body {\n  margin: 0;\n  background: var(--background);",
        "body {\n  margin: 0;\n  background: #ff00ff;",
      );
      grep = "@visual-control";
      expected = /toHaveScreenshot/;
    }
    if (kind === "budget") {
      const payload = Array.from({ length: 10_000 }, (_, index) =>
        createHash("sha256").update(`synthetic-bundle-${index}`).digest("hex"),
      ).join("");
      writeFileSync(
        join(copy, "src/components/budget-payload.ts"),
        `export const payload = ${JSON.stringify(payload)};\n`,
      );
      change(
        copy,
        "src/components/theme-switch.tsx",
        'import { useState } from "react";',
        'import { useState } from "react";\nimport { payload } from "./budget-payload";',
      );
      change(
        copy,
        "src/components/theme-switch.tsx",
        '      variant="secondary"',
        '      data-budget={payload}\n      variant="secondary"',
      );
      grep = "@ui performance";
      expected = /all shipped client JS gzip budget/;
    }
    assert.equal(
      run(copy, `${kind}-build`, [
        "node_modules/next/dist/bin/next",
        "build",
        "--webpack",
      ]),
      0,
      `${kind}: actual mutant production build`,
    );
    env.HARNESS_TEST_REPORT = join(reports, `${kind}.xml`);
    assert.equal(
      run(copy, kind, ["scripts/journeys.ts", "--grep", grep]),
      1,
      `${kind}: expected native assertion failure`,
    );
    const xml = readFileSync(env.HARNESS_TEST_REPORT, "utf8");
    assert.match(xml, /<failure/);
    assert.match(xml, expected, `${kind}: intended control must fail`);
    cpSync(
      join(copy, ".harness/reports/browser"),
      join(reports, `${kind}-artifacts`),
      { recursive: true },
    );
    if (kind === "budget")
      cpSync(
        join(copy, ".harness/reports/performance"),
        join(reports, "budget-measurements"),
        { recursive: true },
      );
    console.log(`${kind}: intended native defect caught`);
  }
} finally {
  rmSync(owned, { recursive: true, force: true });
  console.log(
    "Owned UI mutation source/storage copies removed; maintained baselines untouched.",
  );
  console.log(`Native negative-control evidence: ${reports}`);
}
