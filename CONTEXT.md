# Project Context

One-sentence project description goes here.

## Language

**Operation**: An explicit business action requested by a user or system actor. _Avoid_: handler, service call, button action.

**Invariant**: A rule that must remain true before and after an Operation.

**Verification Ledger**: Volatile evidence in `.claude/state/verification-ledger.md` recording which exact diff hash was checked by which command.

**Target Plugin**: A domain-specific harness extension under `target-plugins/<name>/`.

## Relationships

- An **Operation** changes state through one transaction boundary.
- An **Invariant** is proved by tests or explicitly recorded as unchecked.
- A **Target Plugin** adds specialized skills and verification rules.

## Flagged ambiguities

- "memory" means durable project memory unless explicitly stated as volatile `.claude/state`.
