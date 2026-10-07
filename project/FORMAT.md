# Plan format

Keep one active plan with its tasks in the same file. Use plan IDs such as
`P001` and task IDs such as `P001-T002`. Link to canonical context instead of
copying it into each task.

Each task states its outcome, what to inspect, what to reuse or build,
dependencies, observable proof, and a short reviewer brief. The brief covers
intent, implementation choice, affected boundaries, risk and recovery. Record
actual verification and limitations when completing the task.

Use Complete, In progress, Next or Planned. Complete means the stated outcome
has evidence. A dependency that needs user input or service access belongs in
the task, together with the work that can proceed independently.

This plan organises the harness rebuild. It does not require a new document for
every prompt or small experiment. Future automation must support the agreed
workflow rather than make paperwork a condition for starting Explore work.
