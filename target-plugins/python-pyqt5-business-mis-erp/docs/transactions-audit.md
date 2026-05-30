# Transactions and Audit

State-changing Operations need explicit transaction boundaries.

Audit events should record:

```text
operation name
actor
timestamp source
input summary
entity/document identifiers
before/after where safe and useful
calculation policy version
result or failure
```

Avoid logging secrets and unnecessary personal data.

External side effects after commit must be idempotent or explicitly non-retryable.
