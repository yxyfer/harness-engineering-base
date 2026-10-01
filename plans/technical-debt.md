# Technical Debt

Track intentional compromises that have a concrete impact. Do not use this as a
general wishlist.

| ID | Debt and evidence | Impact | Trigger to address | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TD-000 | Example; replace or delete | TBD | TBD | TBD | open |
| TD-001 | Native static fixture cases share one large contract file (QH-07) | Cohesion review cost as cases grow; no gate suppression | Further distinct fixture families | Repository owner | monitored |
| TD-002 | Verify coordinator retains one linear orchestration function (QH-08) | Cohesion review prompt, not a size gate; adapters/process/identity are separate | Additional control families | Repository owner | monitored |
