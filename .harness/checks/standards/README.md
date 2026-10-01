# Standards check

Detects the configured or present language profiles, reports shared size
thresholds, warns about oversized maintained source, and invokes available shell
and Markdown tools. Python and Node formatter/linter/type checks remain in the
project-command stage so project-owned configuration stays authoritative.

Discovery shares configured directory exclusions and symlink handling with the
other harness-owned scans. Extensionless executable files support direct,
`env`, and `env -S` Python (`python`, `python3`, versioned Python 3) or shell
(`sh`, `bash`, `dash`) shebangs. Unknown interpreters and complex env prefixes
are not guessed as shell. Native commands own other interpreter coverage.

Missing optional tools are reported as degraded coverage rather than silently
treated as a pass. Phase 4 setup/doctor work will make dependency readiness a
separate explicit gate.
