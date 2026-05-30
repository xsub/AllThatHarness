---
name: diagnose
description: Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce, minimise, hypothesise, instrument, fix, regression-test. Use when debugging bugs, failing tests, broken behavior, or performance regressions.
---
# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

Before exploring code, read the project's domain glossary and ADRs for the area.

## Phase 1 — Build a feedback loop

This is the skill. Everything else consumes the loop.

Construct a fast deterministic pass/fail signal before hypothesising. Try, in order:

1. failing test at the seam that reaches the bug
2. CLI or HTTP script with fixture input and expected output
3. headless UI script for GUI symptoms
4. captured trace replay
5. throwaway harness around the code path
6. property/fuzz loop for wrong-output bugs
7. bisect harness for regressions
8. differential loop against old version or config
9. HITL script only as last resort

Improve the loop itself: faster, sharper, more deterministic. Pin time, seed RNG, isolate filesystem, freeze network.

For nondeterministic bugs, raise reproduction rate. Loop 100x, parallelise, stress timing, inject sleeps. A 50% flake is debuggable; 1% is not.

If no loop can be built, stop. List what was tried and request the missing artifact/environment/instrumentation.

## Phase 2 — Reproduce

Run the loop. Confirm it matches the user's reported symptom, not a nearby failure. Capture exact error, output, timing, or UI state.

## Phase 3 — Hypothesise

Generate 3–5 ranked falsifiable hypotheses before testing. Format:

```text
If <cause> is true, then <probe/change> will make the bug disappear or change in <specific way>.
```

Show the ranked list to the user if interactive; proceed with your ranking if not.

## Phase 4 — Instrument

Each probe maps to one hypothesis. Change one variable at a time.

Prefer debugger/REPL, then targeted logs. Never log everything. Prefix all temporary logs with a unique tag like `[DEBUG-a4f2]` and remove them later.

For performance regressions, establish baseline measurement before fixing.

## Phase 5 — Fix + regression test

Write the regression test before the fix when a correct seam exists. Correct seam = the test exercises the real bug pattern as triggered by callers.

If no correct seam exists, record that as an architecture finding and hand off to architecture improvement after the fix.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- original repro no longer reproduces
- regression test passes or absence of seam is documented
- debug instrumentation removed by grepping the unique prefix
- throwaway prototypes deleted or quarantined
- correct hypothesis stated in commit/PR notes
- architectural prevention opportunity recorded if relevant
