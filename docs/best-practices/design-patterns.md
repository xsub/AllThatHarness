# Design Patterns

Use patterns only when the problem has real variation or complexity.

Required adoption record:

```text
Pattern:
Problem:
Variation isolated:
Seam created:
Callers simplified:
Test improved:
New complexity:
Rejected simpler option:
```

Business/MIS/ERP useful patterns:

- Operation/Command for explicit business actions.
- Unit of Work for transaction boundaries.
- Repository only when it expresses domain access, not generic CRUD.
- Adapter for external systems and persistence.
- MVC/MVP for PyQt separation.
- Strategy for pricing/tax/rounding policies with multiple real variants.
