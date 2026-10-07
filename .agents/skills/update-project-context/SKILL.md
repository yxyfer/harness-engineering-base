---
name: update-project-context
description: Reconcile durable repository context after product, architecture, design, data, quality, or security decisions change. Use to prevent plans and chat history becoming the only source of truth.
---

# Update Project Context

Inspect the implemented behaviour, accepted decisions, active or completed plan,
and existing files under `docs/`. Update only facts supported by current evidence.

Put each fact in its canonical file: user outcomes in `PRODUCT.md`, component and
integration boundaries in `ARCHITECTURE.md`, experience rules in `DESIGN.md`,
contracts and provenance in `DATA.md`, verification expectations in `QUALITY.md`,
and trust or control decisions in `SECURITY.md`.

For adopted projects, the shared current architecture lives in
`project/architecture/`: diagram, systems inventory and feature flows.
`docs/ARCHITECTURE.md` may remain a compatibility entry into that view. Update
those maps with source changes, then sync plan/task navigation; keep progress
and historical evidence inside plan bundles, not in canonical architecture.

Add durable trade-offs to `DECISIONS.md` as a new entry. Supersede prior entries
without deleting history. Keep task notes and transient status out of canonical
context; link to plans or evidence instead of copying large logs.

Remove `Status: needs-project-input` only when the document is sufficiently
specific to guide implementation. Run `./harness check` and report any context
still requiring an owner or human decision.
