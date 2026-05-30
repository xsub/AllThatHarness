---
name: tdd
description: Test-driven development using red-green-refactor, one vertical tracer-bullet behavior at a time. Use when building features or fixes test-first.
---
# Test-Driven Development

Core principle: tests verify behavior through public interfaces, not implementation details.

Good tests exercise real code paths and read like specifications. Bad tests mock internal collaborators, test private methods, or break when behavior is unchanged.

## Anti-pattern: horizontal slicing

Do not write all tests first and then all implementation. That tests imagined behavior and locks in premature structure.

Correct pattern:

```text
RED -> GREEN: test1 -> implementation1
RED -> GREEN: test2 -> implementation2
RED -> GREEN: test3 -> implementation3
```

## Workflow

### 1. Planning

Read glossary and ADRs. Confirm public interface and priority behaviors. Identify deep-module opportunities. List behaviors, not implementation steps.

### 2. Tracer bullet

Write one test confirming one end-to-end behavior. Watch it fail. Write minimum code to pass. Watch it pass.

### 3. Incremental loop

For each remaining behavior:

- one test at a time
- only enough code for current test
- no speculative features
- public interface only
- observable behavior only

### 4. Refactor

Only refactor while green. Extract duplication, deepen modules, simplify interfaces, and run tests after each refactor step.

## Per-cycle checklist

- test describes behavior, not implementation
- test uses public interface
- test survives internal refactor
- code is minimal for current test
- no speculative feature added
- verification command recorded
