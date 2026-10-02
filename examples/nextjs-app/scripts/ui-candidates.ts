import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { z } from "zod";

const directory = ".harness/reports/ui-candidates";
const metadata = z
  .object({
    status: z.literal("candidate-not-approved"),
    capture: z.enum(["full-page", "viewport"]),
    sourceDigest: z.string(),
    conditions: z.record(z.string(), z.union([z.string(), z.number()])),
    viewport: z.object({ width: z.number(), height: z.number() }),
    sha256: z.string(),
  })
  .strict();
const images: { name: string; record: z.infer<typeof metadata> }[] = [];
for (const width of [390, 1440])
  for (const theme of ["paper", "ink"])
    for (const state of [
      "list",
      "detail",
      "catalogue",
      "denied",
      "sign-in",
      "invalid",
      "dialog",
      "recovery",
      "saved",
      "viewer",
      "empty",
    ]) {
      const name = `${width}-${theme}-${state}`;
      const record = metadata.parse(
        JSON.parse(readFileSync(`${directory}/${name}.json`, "utf8")),
      );
      assert.equal(
        record.sha256,
        createHash("sha256")
          .update(readFileSync(`${directory}/${name}.png`))
          .digest("hex"),
      );
      if (images.length) {
        assert.equal(
          record.sourceDigest,
          images[0]?.record.sourceDigest,
          "mixed-source candidates",
        );
        assert.deepEqual(
          record.conditions,
          images[0]?.record.conditions,
          "mixed environments",
        );
      }
      images.push({ name, record });
    }
writeFileSync(
  `${directory}/index.html`,
  `<!doctype html><html lang="en"><meta charset="utf-8">
<title>Workroom candidates — NOT approved</title>
<style>body{font:16px Arial;margin:32px}img{max-width:100%;border:1px solid #aaa}section{margin:32px 0}nav{display:flex;flex-wrap:wrap;gap:12px}</style>
<h1>44 review candidates — NOT approved</h1>
<p>Human review is pending. Synthetic Chromium/macOS screenshots; no AI grading.
See tests/visual-baselines/README.md for the deliberate acceptance procedure.</p>
<nav>${images.map(({ name }) => `<a href="#${name}">${name}</a>`).join(" ")}</nav>
${images.map(({ name }) => `<section id="${name}"><h2>${name}</h2><a href="${name}.json">Conditions and SHA-256</a><br><img src="${name}.png" alt="${name} review candidate"></section>`).join("\n")}
</html>`,
);
writeFileSync(
  `${directory}/manifest.json`,
  JSON.stringify(
    {
      status: "candidate-not-approved",
      images,
    },
    null,
    2,
  ),
);
console.log(
  `44 same-source/environment candidate hashes checked; ${directory}/index.html`,
);
