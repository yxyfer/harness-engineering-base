# Reference security

Status: current; foundation only

No authentication or authorization exists. A no-access catalogue card is a
synthetic display, not a security control. No mutation endpoint or real secrets
are supplied. Do not expose this reference as a permissioned production app.
The reviewed npm lock is audited through explicit setup; offline verify consumes
its time/source/version-bound capture. Native secrets/source controls apply.

The external macOS policy denies direct non-loopback networking for verification,
not hostile-code filesystem/IPC escape. Use only trusted synthetic local servers.
No model-provider or production requests belong in tests. Step 11 must implement
and test actual persistence/permission boundaries before claims about saved data.
