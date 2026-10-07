# Lean engineering harness

Build useful software quickly, keep the code readable, and make its architecture
easy to understand. Use Explore, Build or Release according to the intended use
and the consequences of failure.

Start with the [rebuild plan](project/README.md). The
[working agreement](docs/WORKFLOW.md) defines how we code and verify changes. The
[architecture map](docs/ARCHITECTURE.md) distinguishes the current state from
the intended design.

The project was reset in commit `0516ee6`. This rebuild currently contains an
operating agreement and an execution plan. It has no application, installer,
database integration or executable `harness` command yet. The old GitHub CI was
removed. The next task makes native quality checks runnable locally.

The first useful version is a small set of instructions, native tool settings,
and a proven recipe for isolated experiments. A pilot on Next.js, Vercel and
Neon will determine whether that is enough before we add more automation.
