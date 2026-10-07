# Step 10: Build a real Next.js foundation with reusable UI

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** a real production-buildable Next.js example replaces the current
fixture as evidence about Next.js. Keep the lightweight Node fixture for command
routing tests. Suggested new location: `examples/nextjs-app/`, outside managed
harness internals, with its own native scripts and project configuration.

Build only the synthetic work-item list/detail/edit interface and the components
it needs: button, field, error message, dialog/confirmation, navigation and a
simple table/list. Use semantic tokens and two visibly different themes with the
same component APIs. Add loading, empty, error, no-access and success examples.
Keep a small rendered catalogue; do not install a documentation platform just
for it. Use existing customer assets first; no customer assets are assumed here.

**Done when:** the actual app builds and runs; relevant `.tsx` source is
checked; components have interaction tests; both themes reuse the same
implementation; example data is labelled synthetic. Persistence/security are
still pending until Step 11; fixture stubs must not be described as live
integrations.

```text
Implement Step 10 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/10-build-a-real-next-js-foundation-with-reusable-ui.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Add a real Next.js/TypeScript reference app with
compatible pinned dependencies, native scripts and its own harness config.
Retain the lightweight Node dispatcher fixture. Keep example app source outside
managed harness internals and document source/dependency ownership.

Build a small synthetic work-item list/detail/edit UI using an approved local
component kit, semantic tokens and two themes sharing component implementations.
Prefer existing assets; otherwise use a small owned shadcn-based foundation with
one primitive stack. Add only needed controls and loading/empty/error/no-access/
success examples. Keep browser state in small Client Components and use Server
Components appropriately. Document components, variants and reuse rules.

Run the real production build and initial component/navigation checks. Label
stubbed data and pending persistence/auth accurately. Populate relevant design
context, write project/plans/P002-quality-first-harness/evidence/QH-10.md, and stop.
```
