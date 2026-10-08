# Engineering debt

## Next.js lint compatibility during adoption

Observed in the T002 validation app on 2026-10-07: Next.js 16.4.0's native lint
configuration resolved React lint plugin 7.37.5, which declares ESLint support
through version 9. The app used ESLint 9.39.5 for that configuration, which is
[out of maintenance](https://eslint.org/version-support/). Kit JavaScript uses
the maintained ESLint 10 line. The validation app and its ESLint 9 installation
have been removed; this remains an adoption constraint to review in a receiving
application.

Recheck the receiving app's React plugin and Next.js config before adoption.
Upgrade when their peer ranges and actual lint checks support ESLint 10. Keep
React and hooks checks enabled; do not use a forced peer install to hide this.
This debt concerns development tooling, not a verified application
vulnerability.
