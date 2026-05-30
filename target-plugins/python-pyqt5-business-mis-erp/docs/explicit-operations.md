# Explicit Operations

An Operation is a business verb. Examples:

- CreateInvoice
- PostPayment
- ReserveStock
- ReleaseReservation
- ApprovePurchaseOrder
- RecalculateDocumentTotals

Do not use vague names like `save`, `process`, `handle`, or `update` when a domain verb exists.

Operation implementation must declare input, validation, protected invariants, calculation policy, persistence boundary, audit event, result, and failure modes.
