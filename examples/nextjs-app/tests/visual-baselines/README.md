# Visual baseline ownership

No images have been accepted yet. `.harness/reports/ui-candidates/` contains
review candidates, not approved baselines. The required `@visual-approved`
native cases fail until a human reviews every image and intentionally commits
the chosen PNGs here with `approval.json`.

The approval object has `status: "human-accepted"`, a named `reviewer`, ISO UTC
`acceptedAt`, exact `conditions` copied from candidate metadata, and `images`
mapping each image basename (without `.png`) to its SHA-256. Every matrix/state
image must be present. Source/config/lock and accepted images are fingerprinted
by verify. Review the tested source alongside candidates; approval is unsigned
repository evidence, not proof of who actually reviewed it.

Use Chromium 153.0.8010.12 / Playwright 1.63.0 on the recorded macOS arm64
release. Viewports are 390×1000 and 1440×1000, DPR 1; Paper/Ink share components.
Locale en-GB, UTC, local Arial/Helvetica, reduced motion, hidden screenshot
caret and disabled animations. Dialogs capture the actual viewport, not a
stitched document with a misleading fixed overlay; other states are full-page.
No masks or image-region exclusions. Native
pixelmatch YIQ threshold 0.1 ignores only small colour distance; zero pixels
above that threshold are allowed. No automatic baseline writes, retries or
accepted-diff updates. An OS/font/browser upgrade requires deliberate review.

Automated comparisons detect changes, not visual quality. Axe WCAG 2 A/AA and
2.1 A/AA scans do not establish conformance; review incomplete checks, screen
reader behaviour, zoom, cognitive usability and real assistive technology.
Firefox/WebKit remain unverified. Catalogue loading/success cards are explicitly
synthetic presentations; server loading timing is not controlled by a UI mock.
