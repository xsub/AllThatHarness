---
name: one-change-at-a-time
description: Enforce one semantic change per edit cycle with verification before continuing. Use for all implementation work.
---
# One Change At A Time

A semantic change is one behavior, invariant, refactor step, or config change.

Loop:

1. State intended change.
2. Identify invariant.
3. Edit the minimum files.
4. Run focused verification.
5. Record command and result.
6. Continue only if green.

Forbidden:

- broad rewrites before a passing baseline
- mixing refactor and behavior change
- fixing unrelated issues opportunistically
- batching several features under one verification
