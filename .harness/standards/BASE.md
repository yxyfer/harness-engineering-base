# Engineering baseline

Follow [the working agreement](../../docs/WORKFLOW.md). Native tool settings are
authoritative for formatting and static checks.

- Run the formatter first. Default to 80 columns and two-space indentation.
- Give each function, module and dependency a clear purpose. Prefer the smallest
  coherent change over extra layers or arbitrary file splitting.
- Review functions above 50 lines and files above 350 maintained source lines
  for cohesion. These are review prompts, not automatic failures.
- Preserve unrelated work. Keep secrets and machine-specific paths out of
  committed configuration. Mark synthetic data and simulated behaviour.
- A failing command is a failed check. Fix the cause; do not suppress it to make
  the task appear complete. Report unavailable checks explicitly.
