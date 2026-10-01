# Demo integrity check

Looks for strong live/production claims in text artifacts. If such claims exist,
the project must have a data context that explicitly distinguishes real and
simulated behaviour. This is a guardrail, not proof that every claim is true.

The existing text-extension scope uses shared configured directory exclusions
and skips symlinks. Required classification context cannot use a symlink.
