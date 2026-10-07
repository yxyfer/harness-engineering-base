# Step 03: Unify discovery and honour command precedence

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** files reach the correct tools and project commands control their
promised scope. Fix F3–F5 with shared harness-owned path discovery. Define
root-relative versus directory-component exclusions and symlink handling. Native
tools keep their own exclusions. Mandatory policy checks remain separate from
the single resolved project static-check implementation.

**Done when:** extensionless Python avoids shell tools; nested exclusions apply
consistently; excluded trees are pruned; traversal stays inside the intended
root; paths with spaces work; project overrides run once; policy failures block.

```text
Implement Step 03 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/03-unify-discovery-and-honour-command-precedence.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md and reproduce F3, F4 and F5 first.

Create the smallest shared walker/classifier needed by harness-owned checks.
Route supported shebangs correctly, define exclusion semantics, prune ignored
trees and prevent symlink escapes. Keep native tool configuration authoritative
for native scope. Resolve one project static-check implementation after required
policy checks. An explicit project override must not trigger automatic Python
checking as an additional hidden stage.

Test extensionless Python/shell, nested exclusions, spaced paths, symlinks,
failing mandatory policy and exactly-once project command invocation. Run real
installed tools where possible; report missing coverage. Reconcile the managed
inventory, write project/plans/P002-quality-first-harness/evidence/QH-03.md, and stop.
```
