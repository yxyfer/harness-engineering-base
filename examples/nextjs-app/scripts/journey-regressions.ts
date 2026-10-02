import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
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

// Mechanical mutations affect generated disposable copies only. Never modify
// the maintained app or turn an arbitrary failed setup into a mutation pass.
const source = resolve(".");
const owned = mkdtempSync(join(realpathSync(tmpdir()), "workroom-mutants-"));
const reports = resolve(".harness/reports/journey-regressions");
mkdirSync(reports, { recursive: true });
const env: NodeJS.ProcessEnv = {
  ...process.env,
  PLAYWRIGHT_BROWSERS_PATH: resolve(".harness/tmp/browsers"),
};

function run(cwd: string, name: string, argv: string[]) {
  const result = spawnSync(process.execPath, argv, {
    cwd,
    env,
    timeout: 180_000,
    encoding: "utf8",
    maxBuffer: 4 * 1024 * 1024,
  });
  const output = result.stdout + result.stderr;
  writeFileSync(join(reports, `${name}.log`), output.slice(0, 65_536));
  assert(!result.error && !result.signal, `${name}: runner/setup failed`);
  return result;
}

function change(cwd: string, file: string, before: string, after: string) {
  const path = join(cwd, file);
  const text = readFileSync(path, "utf8");
  assert.equal(text.split(before).length, 2, "mutation anchor must be unique");
  writeFileSync(path, text.replace(before, after));
}

try {
  for (const kind of ["save", "access"] as const) {
    const copy = join(owned, kind);
    mkdirSync(copy);
    const excluded = ["node_modules", ".next", "tmp", "reports", ".git"];
    for (const name of readdirSync(source)) {
      if (excluded.includes(name)) continue;
      if (name === ".harness") {
        mkdirSync(join(copy, name));
        for (const input of readdirSync(join(source, name))) {
          if (!excluded.includes(input))
            cpSync(join(source, name, input), join(copy, name, input), {
              recursive: true,
            });
        }
      } else
        cpSync(join(source, name), join(copy, name), {
          recursive: true,
          filter: (path) => !excluded.includes(basename(path)),
        });
    }
    // Reuse the already locked installed tools, never download during tests.
    symlinkSync(
      join(source, "node_modules"),
      join(copy, "node_modules"),
      "dir",
    );
    if (kind === "save") {
      change(
        copy,
        "src/server/work-items.ts",
        `      db.prepare(
        "UPDATE work_items SET title=?,status=?,version=version+1 WHERE id=? AND version=?",
      ).run(input.title, input.status, id, input.version);
      db.prepare(
        "INSERT INTO audit(item_id,actor_id,version) VALUES(?,?,?)",
      ).run(id, principal.id, input.version + 1);`,
        "      // Deliberately broken save: return success without a commit.",
      );
    } else {
      change(
        copy,
        "src/domain/access.ts",
        "principal.id === resource.ownerId &&",
        "principal.id.length > 0 &&",
      );
    }
    const build = run(copy, `${kind}-build`, [
      "node_modules/next/dist/bin/next",
      "build",
      "--webpack",
    ]);
    assert.equal(build.status, 0, `${kind}: mutant must build before grading`);
    const report = join(reports, `${kind}.xml`);
    env.HARNESS_TEST_REPORT = report;
    const result = run(
      copy,
      kind,
      kind === "save"
        ? ["scripts/journeys.ts", "--grep", "@smoke"]
        : [
            "node_modules/vitest/vitest.mjs",
            "run",
            "--config",
            "vitest.server.config.ts",
            "--testNamePattern",
            "wrong owners",
            "--outputFile.junit",
            report,
          ],
    );
    assert.equal(result.status, 1, `${kind}: expected assertion failure`);
    const xml = readFileSync(report, "utf8");
    assert.match(xml, /<failure/, `${kind}: native failure evidence required`);
    assert.match(
      xml,
      kind === "save" ? /An updated saved title/ : /expected 200 to be 404/,
      `${kind}: must fail for intended behaviour, not infrastructure`,
    );
    if (kind === "save") {
      // A browser error must fail even when the user assertions otherwise pass.
      // Reuse the original healthy production artifact in this owned copy.
      rmSync(join(copy, ".next"), { recursive: true, force: true });
      cpSync(join(source, ".next"), join(copy, ".next"), { recursive: true });
      change(
        copy,
        "tests/navigation/navigation.test.ts",
        '  await page.goto("/sign-in");',
        '  await page.goto("/sign-in");\n  await page.evaluate(() => { console.error("synthetic unexpected browser error"); queueMicrotask(() => { throw new Error("synthetic unexpected page error"); }); });',
      );
      env.HARNESS_TEST_REPORT = join(reports, "browser-error.xml");
      const guard = run(copy, "browser-error", [
        "scripts/journeys.ts",
        "--grep",
        "@smoke",
      ]);
      assert.equal(guard.status, 1);
      assert.match(
        readFileSync(env.HARNESS_TEST_REPORT, "utf8"),
        /unexpected browser errors/,
      );
      assert.match(
        readFileSync(env.HARNESS_TEST_REPORT, "utf8"),
        /synthetic unexpected page error/,
      );
    }
    console.log(
      `${kind}: intended regression caught; native evidence retained`,
    );
  }
} finally {
  rmSync(owned, { recursive: true, force: true });
  console.log("Disposable mutation source/storage copies removed.");
}
