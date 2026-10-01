# Lightweight measurement record

Copy one record per attempted check or bounded task into that step's evidence.
This is a recording convention, not a runtime schema or new harness command.
Leave unobserved fields `null`; zero means measured zero. Preserve failed first
attempts and append retries with the same run ID and increasing attempt number.

```json
{
  "run_id": "QH-NN-case-id",
  "attempt": 1,
  "step": "NN",
  "case_ids": [],
  "started_at": "ISO-8601 with offset",
  "source": {"head": null, "dirty_digest": null, "config_lock_digests": {}},
  "environment": {"os": null, "runtimes_tools": {}, "cache_state": "unknown"},
  "scope": "native | harness wrapper | foundation | full journey",
  "command": [],
  "cwd": "repository-relative or disposable target label",
  "exit": null,
  "status": "passed | failed | unavailable | skipped | not-applicable",
  "reason": null,
  "collected": null,
  "passed": null,
  "failed": null,
  "skipped": null,
  "feedback_seconds": null,
  "feedback_method": "monotonic elapsed command-to-completion",
  "human_minutes": {
    "implementation": null, "review": null, "correction": null,
    "setup": null, "maintenance": null, "context": null
  },
  "task_acceptance": null,
  "escaped_defects": null,
  "seeded_defects_detected_missed": null,
  "false_failure_or_flaky": null,
  "human_product_design_acceptance": null,
  "evidence": []
}
```

Record human effort contemporaneously with start/stop intervals and who measured
it. Do not reconstruct it from Git/chat timestamps or agent elapsed time. Count
setup, documentation, maintenance, failed attempts, review and correction costs.
Use `unavailable` for absent/broken prerequisites; `skipped` for an available
check that was not executed, and `not-applicable` only with a concrete reason.
A zero exit with missing controls is a partial result, not full acceptance.

Compare native commands and the wrapper on the same source, cases, tools and
environment. Record foundation reuse separately; do not attribute component
benefits to command routing. Label cache state as cold/warm only when observed.
Agree a feedback budget from observed use at Step 17. Retain distributions and
case-level failures; a single run cannot establish a speedup or productivity gain.
