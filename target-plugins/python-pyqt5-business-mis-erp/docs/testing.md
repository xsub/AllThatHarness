# Testing

## Required test classes

- Decimal calculation vectors.
- Operation success/failure tests.
- Transaction rollback tests.
- Audit-event tests for state-changing Operations.
- Qt model data/setData/signal tests.
- Critical widget smoke tests with pytest-qt.

## Headless Qt

Use:

```bash
QT_QPA_PLATFORM=offscreen python3 -m pytest -q
```

## Test names

Use domain language:

```text
test_invoice_total_uses_line_rounding_policy
test_post_payment_rejects_overpayment
test_stock_reservation_rolls_back_when_audit_write_fails
```
