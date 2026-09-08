---
name: reproduce-bug
description: Reproduce and isolate a reported software defect with minimal evidence. Use when the requested outcome is diagnosis or a stable failing test, not automatically a fix.
---

# Reproduce Bug

Read the report, `AGENTS.md`, relevant project context, and nearby implementation.
Separate observed facts from hypotheses. Do not change production behaviour when
the request is diagnosis only.

Capture the environment and reduce the report to the smallest deterministic
sequence. Establish expected versus actual behaviour, then reproduce through the
closest existing test boundary. Prefer a failing automated test when it reflects
the user-visible defect without overfitting to an implementation detail.

Vary one condition at a time to localise the failure. Check error, empty,
permission, timing, and data-shape paths only where evidence points.

Report the exact reproduction, evidence, suspected boundary, confidence, and
remaining unknowns. If a fix is also requested, preserve the failing test, make
the smallest correction, and demonstrate it now passes without hiding regressions.
