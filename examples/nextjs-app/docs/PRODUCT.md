# Reference product

Production Chromium now proves the local authenticated main and recovery
journeys, including durable save/reload and denied edits. These are synthetic
local sessions and storage, not external SSO or production product acceptance.

Status: current

A synthetic work-item workspace with real disposable SQLite, password sign-in,
database-backed sessions and authorized saves. Users see only owned same-tenant
work; editors save and viewers read. Refresh/restart retains committed changes.
No customer records, external SSO, live service or deployment is implemented.
