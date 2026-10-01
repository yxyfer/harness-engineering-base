# Architecture standard

- Keep modules cohesive around one reason to change and direct dependencies
  toward stable domain policy.
- Separate deterministic decisions from external I/O where that makes behaviour
  easier to test and reason about.
- Put stable, narrow interfaces at volatile boundaries such as vendors,
  persistence, network services, and model providers.
- Prefer the simplest design that satisfies demonstrated needs (KISS and YAGNI).
- Apply DRY to shared knowledge, not coincidental syntax. Duplication is often
  safer than a premature abstraction; consolidate when the common concept and
  change pattern are clear.
- Grant the least privilege needed and make consequential operations explicit.
- Make failures diagnosable with useful, non-sensitive logs and health signals.
- Evolve stored data and public interfaces compatibly. Define migration,
  rollback, or safe-forward recovery before risky changes.
- Preserve provenance across derived data, generated outputs, and simulated
  integrations.

Create an ADR when a choice changes system boundaries, dependencies, security or
privacy posture, stored-data compatibility, externally consumed interfaces, or
a standard that future work would otherwise repeatedly debate. Local reversible
implementation choices do not need an ADR.
