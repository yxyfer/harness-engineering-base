# Security Context

Step 06 does not implement security scanning. Schema 1 security.mode is
deprecated with an explicit no-assurance diagnostic. Schema 2 off reports no
scanner assurance, while local/ci return unsupported and require SECURITY
context. Capability-derived security requirements cannot be disabled by mode.

Status: needs-project-input

## Trust boundaries

Describe users, services, external systems, and where trust changes.

## Sensitive assets

| Asset | Sensitivity | Access rule | Protection | Audit evidence |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## Threats and controls

Cover authentication, authorization, injection, secret handling, dependency risk,
data exposure, abuse, logging, and recovery where relevant.

## Human approval gates

Record actions that require confirmation, the information shown to the approver,
and how approval is audited.

## Incident and disclosure path

Document who owns response, how access can be revoked, and how affected users or
systems are identified.
