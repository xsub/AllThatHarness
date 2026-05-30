---
name: transactional-persistence
description: Define explicit transaction boundaries, unit-of-work behavior, repositories, audit events, and rollback semantics. Use when touching database writes, SQLAlchemy, sqlite3, migrations, or persistence adapters.
---
# Transactional Persistence

Every state-changing Operation must define its transaction boundary.

Rules:

- no implicit multi-step writes outside a UnitOfWork
- one commit point per Operation unless explicitly justified
- rollback on validation, invariant, persistence, and audit failure
- repositories do not decide business policy
- audit event is written in the same transaction when it describes the state change
- external side effects after commit require idempotency and retry strategy
- do not leave sessions/connections open across unrelated UI events

Record:

```text
Transaction starts:
Rows/entities changed:
Audit written:
Commit point:
Rollback conditions:
Idempotency/retry handling:
```
