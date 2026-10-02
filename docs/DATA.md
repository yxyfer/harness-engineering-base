# Data Context

## Harness verification artifacts

Step 09 setup records public PyPI/npm native advisory data in fixed ignored
reports/advisories. Source/time, tool version, lock/manifest identity, native
collection and capture hash are required; 24h freshness is enforced. Capture
bytes join verification inputs. Sanitized findings omit secret values/snippets.
Tests generate synthetic token/advisory fixtures; live setup is separate. No
production/model integration or cloud export is introduced.

Step 08 uses local synthetic test data and native runner evidence. The versioned
contract is `.harness/verification/schema.json`; output lives in fixed ignored
`.harness/reports/verify-*/` directories. Reports hold source/config/environment
hashes, collection outcomes, commands, versions and redacted artifact identities,
not source contents. No cloud export, durable database or production dataset is
introduced. Retention/removal is local owner responsibility; no cleanup deletes
project-owned reports. Stale-input validation is provenance, not authenticity.

Status: needs-project-input

## Data classes

| Dataset or entity | Owner | Source | Classification | Retention |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## Contracts

Link to schemas and describe identifiers, required fields, lifecycle, validation,
and compatibility expectations.

## Provenance

For every material output, preserve or expose the source, retrieval time,
transformation, confidence or limitations, and whether data is real, synthetic,
modelled, or simulated.

## Storage and movement

Describe persistence, caching, regional boundaries, exports, deletion, and
recovery.

## Test and demo data

State how non-production data is generated, labelled, and kept separate from live
data.
