---
name: explicit-business-operation
description: Model each business action as an explicit Operation with input DTO, validation, invariants, calculation policy, transaction boundary, audit event, result DTO, and tests. Use for ERP/MIS workflows and state changes.
---
# Explicit Business Operation

An Operation is the only place where a business action changes state.

Operation record:

```text
Name:
Actor:
Intent:
Input DTO:
Authorization:
Validation:
Preconditions:
Invariants protected:
Calculation policy:
Transaction boundary:
State changes:
Audit event:
Result DTO:
Failure modes:
Idempotency key if external/retryable:
```

Implementation rules:

- one Operation per user/business intent
- no hidden side effects in widgets, models, delegates, repositories, or validators
- Operation returns a result object, not raw UI mutation
- errors are explicit and typed/domain-named
- transaction opens and commits inside Operation or UnitOfWork boundary
- audit event names use domain language
- tests call Operation directly without Qt where possible
