---
name: visual-qa
description: Verify an implemented interface across required states and viewports using rendered evidence and interaction checks. Use after visual UI changes or for a focused visual audit.
---

# Visual QA

Read the task acceptance criteria and `docs/DESIGN.md`. Identify the smallest
matrix of routes, states, and viewports that covers the changed experience,
including relevant empty, loading, error, focus, and permission states.

Start the project with `./harness start` and capture fresh rendered evidence. Check
layout, hierarchy, clipping, overflow, responsive reflow, content accuracy,
keyboard focus, semantics, contrast, and reduced motion where applicable. Inspect
the actual interaction rather than judging source code alone.

Compare against approved components and references, allowing intentional
responsive differences. Record each issue with route, viewport, state,
reproduction, impact, and screenshot. Do not silently alter product or design
decisions during an audit.

After requested fixes, repeat the affected matrix and link the before/after
evidence in the verification report.
