# Calculation Precision

Business calculations must be exact, explicit, and testable.

## Money and decimal-like values

Use Decimal for:

- money
- tax
- discounts
- quantities with fractional units
- exchange rates
- unit prices
- stock valuation
- allocations

Do not use float for these values. Do not use Qt double validators as domain validation.

## Rounding policy

Rounding is a named policy:

```text
name:
scale:
rounding mode:
rounding timing:
scope:
effective date:
examples:
```

## Test vectors

Every nontrivial calculation needs vectors:

```text
input -> expected output -> reason
```

Include ties, boundaries, zero, negative, large values, and multi-line aggregation cases.
