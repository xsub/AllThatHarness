# Target: Python PyQt5 Business MIS/ERP

This target specializes Claude Code for desktop business information systems: ERP, MIS, accounting-adjacent workflows, inventory, invoicing, purchasing, sales, stock, settlement, reporting, approvals, and administrative back-office software.

## Non-negotiable rules

1. Business actions are explicit **Operations**.
2. Operations own validation, authorization, invariant checks, transaction boundary, audit event, and result.
3. Widgets do not contain business rules or calculations.
4. Money, tax, quantity, discount, exchange-rate, and accounting-like values use `Decimal`, never binary float.
5. Rounding is a named policy with scale, mode, timing, legal/business rationale, and test vectors.
6. Qt validators are UI constraints only; domain validation must still run inside Operations.
7. Persistence writes are inside explicit transactions.
8. Every state-changing Operation emits an audit event or records why no audit is needed.
9. Tests include deterministic calculation vectors and GUI smoke tests for critical flows.
10. Every calculation formula is explicit and reviewable.

## Architecture shape

```text
UI widgets/views/delegates
  -> Qt models / presenters
  -> application Operations
  -> domain calculations and policies
  -> repositories / unit of work
  -> database / external adapters
```

The domain layer must run without Qt.

## Explicit Operation shape

```text
Operation name:
Actor:
Input DTO:
Preconditions:
Validation rules:
Calculation policy:
Transaction boundary:
State changes:
Audit event:
Result DTO:
Failure modes:
Tests:
```

## Calculation policy shape

```text
Formula name:
Inputs:
Decimal scale:
Rounding mode:
Rounding timing:
Tax/discount/order rule:
Effective date:
Examples:
Rejected alternatives:
```
