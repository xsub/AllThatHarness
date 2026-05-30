---
name: grill-with-docs
description: Stress-test a plan against project language, code, and ADRs. Updates CONTEXT.md and ADRs inline when decisions crystallize. Use before nontrivial changes.
---
# Grill With Docs

Interview the plan relentlessly until shared understanding exists.

Walk one branch of the design tree at a time. For each question, provide your recommended answer. Ask one question at a time. If code can answer the question, inspect code instead of asking.

## Domain awareness

Look for:

```text
CONTEXT.md
CONTEXT-MAP.md
docs/adr/
src/*/CONTEXT.md
src/*/docs/adr/
```

Create files lazily only when there is something concrete to write.

## During the session

- challenge terms that conflict with `CONTEXT.md`
- sharpen vague terms into canonical domain language
- test domain relationships with concrete scenarios and edge cases
- cross-check user claims against code when possible
- update `CONTEXT.md` immediately when a term is resolved
- do not couple `CONTEXT.md` to implementation details

## ADR rule

Offer an ADR only when all are true:

1. hard to reverse
2. surprising without context
3. result of a real tradeoff

If any is false, skip the ADR.
