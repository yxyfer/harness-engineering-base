# Standards check

Detects the configured or present language profiles, reports shared size
thresholds, warns about oversized maintained source, and invokes available shell
and Markdown tools. Python and Node formatter/linter/type checks remain in the
project-command stage so project-owned configuration stays authoritative.

Missing optional tools are reported as degraded coverage rather than silently
treated as a pass. Phase 4 setup/doctor work will make dependency readiness a
separate explicit gate.
