---
name: business-decimal-precision
description: Enforce exact Decimal arithmetic for money, tax, quantity, price, discount, exchange rate, and accounting-like business calculations. Use whenever calculations, totals, invoices, stock valuation, or rounding are involved.
---
# Business Decimal Precision

No binary float for business values.

Use `Decimal` from strings, integers, or stored exact text/integer minor units. Never construct `Decimal` from `float`.

Every calculation must define:

```text
Formula:
Inputs:
Scale:
Rounding mode:
Rounding timing:
Effective date or policy version:
Examples:
```

Rules:

- quantize at explicit policy boundaries, not randomly after every expression
- keep intermediate precision high enough for the formula
- trap `FloatOperation` in tests and calculation contexts
- test positive, zero, negative, boundary, and tie cases
- test legal/business rounding examples as golden vectors
- make display formatting separate from stored/calculated value
- never use `QDoubleValidator` as domain validation for money

Use `money.py` template as a starting point, not as a universal model.
